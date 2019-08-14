using lmaocore;
using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    public class DatabaseService
    {
        private readonly BotConfig Config;

        private MongoClient Mongo;
        private IMongoDatabase Database;

        private Dictionary<long, string> prefixes;
        //TODO: We need to cache local server settings until we know an update has occurred to it's not calling mongo every time

        public DatabaseService(BotConfig config)
        {
            Config = config;

            //Mongo Connection String: mongodb://user:password@hostname:port
            Mongo = new MongoClient(String.Format("mongodb://{0}:{1}@{2}:{3}", Config.Mongo.User, Config.Mongo.Password, Config.Mongo.Hostname, Config.Mongo.Port));
            Database = Mongo.GetDatabase(config.Mongo.Database);
            GetPrefixes();
        }

        /// <summary>
        /// Downloads the entire server collection from Mongo and parses for just prefixes
        /// so that we don't need to search for a prefix on every damn message.
        /// </summary>
        public async Task<Dictionary<long, string>> GetPrefixes()
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.ServerSettings>("servers");
            List<lmaocore.Models.ServerSettings.ServerSettings> servers = (await collection.FindAsync(new BsonDocument())).ToList();
            prefixes = new Dictionary<long, string>();

            foreach (lmaocore.Models.ServerSettings.ServerSettings server in servers)
            {
                prefixes.Add(server.ServerID, server.BotSettings.CommandPrefix);
            }
            return prefixes;
        }

        /// <summary>
        /// Get the prefix for the specified server from a cache if available,
        /// otherwise Mongo.
        /// </summary>
        /// <param name="serverID">The ID of the server</param>
        /// <returns>The prefix for the specified server</returns>
        public async Task<string> GetPrefix(long serverID)
        {
            if (prefixes.ContainsKey(serverID)) return prefixes[serverID];
            else
            {
                //We don't have the prefix cached. Let's see if we can grab it from mongo.
                //This can happen if there is a new server
                var collection = Database.GetCollection<lmaocore.Models.ServerSettings.ServerSettings>("servers");
                var filter = Builders<lmaocore.Models.ServerSettings.ServerSettings>.Filter.Eq("ServerID", serverID);

                if (await collection.CountDocumentsAsync(filter) == 1)
                {
                    string prefix = (await collection.FindAsync(filter)).First().BotSettings.CommandPrefix;
                    prefixes.Add(serverID, prefix);
                    return prefix;
                }
                else
                {
                    //Not found in Mongo either. This shouldn't happen. Return lmao.
                    //It is not the job of GetPrefix() to create a new settings object if it doesn't exist.
                    //Log.LogString("Attempted to find prefix for " + serverID + " but none could be found!");
                    return "lmao";
                }
            }
        }

        /// <summary>
        /// Increments the usage count of a command by one
        /// </summary>
        /// <param name="command">The command to increment</param>
        public async Task UpdateUsageCount(string command)
        {
            var collection = Database.GetCollection<lmaocore.Models.CommandUsage>("usage");
            var filter = Builders<lmaocore.Models.CommandUsage>.Filter.Eq("Command", command);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                var update = Builders<lmaocore.Models.CommandUsage>.Update.Inc("Uses", 1);
                await collection.UpdateOneAsync(filter, update);
            }
            else
            {
                await collection.InsertOneAsync(new lmaocore.Models.CommandUsage()
                {
                    Command = command,
                    Uses = 1,
                    SubCommands = null
                });
            }
        }

        /// <summary>
        /// Update the lmao count of the specified user
        /// </summary>
        /// <param name="userID">The ID of the user to update</param>
        public async Task UpdateLmaoCount(long userID)
        {
            var collection = Database.GetCollection<lmaocore.Models.UserSettings.UserSettings>("users");
            var filter = Builders<lmaocore.Models.UserSettings.UserSettings>.Filter.Eq("UserID", userID);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                var update = Builders<lmaocore.Models.UserSettings.UserSettings>.Update.Inc("Settings.LmaoCount", 1);
                await collection.UpdateOneAsync(filter, update);
            }
            else
            {
                await collection.InsertOneAsync(new lmaocore.Models.UserSettings.UserSettings()
                {
                    UserID = userID,
                    Settings = new lmaocore.Models.UserSettings.Settings()
                    {
                        LmaoCount = 1
                    },
                    Reminders = null
                });
            }
        }

        /// <summary>
        /// Retrieves the server settings for the specified ID
        /// </summary>
        /// <param name="serverID">The ID of the server</param>
        /// <returns>The specified server settings</returns>
        public async Task<lmaocore.Models.ServerSettings.ServerSettings> GetServerSettings(long serverID)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.ServerSettings>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.ServerSettings>.Filter.Eq("ServerID", serverID);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                lmaocore.Models.ServerSettings.ServerSettings serverSettings = await collection.Find(filter).FirstAsync();
                //Might as well update the prefix while we're at it
                if (!prefixes[serverID].Equals(serverSettings.BotSettings.CommandPrefix)) prefixes[serverID] = serverSettings.BotSettings.CommandPrefix;
                return serverSettings;
            }
            else
            {
                //Server doesn't have any settings saved. Could happen because of corrupted import.
                //For now we're just gonna return an empty one, and we'll be sure to upload it to the database
                lmaocore.Models.ServerSettings.ServerSettings serverSettings = new lmaocore.Models.ServerSettings.ServerSettings()
                {
                    ServerID = serverID,
                    BotSettings = new lmaocore.Models.ServerSettings.BotSettings()
                    {
                        AllowNSFW = false,
                        CommandPrefix = "lmao",
                        LastModified = DateTime.Now,
                        ReactChance = 100,
                        ReplaceAssChance = 100
                    },
                    CustomCommands = null,
                    Filters = null,
                    LmaoAdmins = new List<string>()
                };
                await collection.InsertOneAsync(serverSettings);
                //Log.LogString("Tried to fetch server settings from database but it did not exist: " + serverID);
                return serverSettings;
            }
        }

        /// <summary>
        /// Get the bot settings of the specified user
        /// </summary>
        /// <param name="userID">the ID of the user to get</param>
        /// <returns>The UserSettings model of the user</returns>
        public async Task<lmaocore.Models.UserSettings.UserSettings> GetUserSettings(long userID)
        {
            var collection = Database.GetCollection<lmaocore.Models.UserSettings.UserSettings>("users");
            var filter = Builders<lmaocore.Models.UserSettings.UserSettings>.Filter.Eq("UserID", userID);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                lmaocore.Models.UserSettings.UserSettings settings = await collection.Find(filter).FirstAsync();
                return settings;
            }
            else
            {
                //No settings saved, we'll make new one
                return new lmaocore.Models.UserSettings.UserSettings()
                {
                    Reminders = null,
                    UserID = userID,
                    Settings = new lmaocore.Models.UserSettings.Settings()
                    {
                        LmaoCount = 0
                    }
                };
            }
        }

        public async Task SaveUserSettings(lmaocore.Models.UserSettings.UserSettings settings, SaveUserSettingsOptions options)
        {
            var collection = Database.GetCollection<lmaocore.Models.UserSettings.UserSettings>("users");
            var filter = Builders<lmaocore.Models.UserSettings.UserSettings>.Filter.Eq("UserID", settings.UserID);

            var update = Builders<lmaocore.Models.UserSettings.UserSettings>.Update;
            var updates = new List<UpdateDefinition<lmaocore.Models.UserSettings.UserSettings>>();

            if (options.UpdateUserReminders) updates.Add(update.Set("Reminders", settings.Reminders));
            if (options.UpdateUserLmaoCount) updates.Add(update.Set("Settings.LmaoCount", settings.Settings.LmaoCount));

            await collection.FindOneAndUpdateAsync<lmaocore.Models.UserSettings.UserSettings>(filter, update.Combine(updates));
        }

        public async Task SaveServerSettings(lmaocore.Models.ServerSettings.ServerSettings settings, SaveServerSettingsOptions options)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.ServerSettings>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.ServerSettings>.Filter.Eq("ServerID", settings.ServerID);

            var update = Builders<lmaocore.Models.ServerSettings.ServerSettings>.Update;
            var updates = new List<UpdateDefinition<lmaocore.Models.ServerSettings.ServerSettings>>();

            if (options.BotSettingsOptions != null)
            {
                if (options.BotSettingsOptions.UpdateCommandPrefix) updates.Add(update.Set("BotSettings.CommandPrefix", settings.BotSettings.CommandPrefix));
                if (options.BotSettingsOptions.UpdateReplaceAssChance) updates.Add(update.Set("BotSettings.ReplaceAssChance", settings.BotSettings.ReplaceAssChance));
                if (options.BotSettingsOptions.UpdateReactChance) updates.Add(update.Set("BotSettings.ReactChance", settings.BotSettings.ReactChance));
                if (options.BotSettingsOptions.UpdateAllowNSFW) updates.Add(update.Set("BotSettings.AllowNSFW", settings.BotSettings.AllowNSFW));
                updates.Add(update.Set("BotSettings.LastModified", DateTime.Now));
            }
            if (options.SaveLmaoAdmins) updates.Add(update.Set("LmaoAdmins", settings.LmaoAdmins));
            if (options.SaveFilters) updates.Add(update.Set("Filters", settings.Filters));
            if (options.SaveCustomCommands) updates.Add(update.Set("CustomCommands", settings.CustomCommands));

            await collection.FindOneAndUpdateAsync<lmaocore.Models.ServerSettings.ServerSettings>(filter, update.Combine(updates));
        }
    }

    public class SaveUserSettingsOptions
    {
        public bool UpdateUserReminders = false;
        public bool UpdateUserLmaoCount = false;
    }

    public class SaveServerSettingsOptions
    {
        public SaveBotSettingsOptions BotSettingsOptions = null;
        public bool SaveLmaoAdmins = false;
        public bool SaveFilters = false;
        public bool SaveCustomCommands = false;
    }

    public class SaveBotSettingsOptions
    {
        public bool UpdateCommandPrefix = false;
        public bool UpdateReplaceAssChance = false;
        public bool UpdateReactChance = false;
        public bool UpdateAllowNSFW = false;
        //if any of these are true, last modified should be updated.
    }
}

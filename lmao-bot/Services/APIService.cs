using Discord.Commands;
using lmaocore;
using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Flurl;

namespace lmao_bot.Services
{
    public class APIService
    {
        private readonly LogService Log;
        private readonly Config Config;

        private string Url;

        private Dictionary<long, string> prefixes;
        //TODO: We need to cache local server settings until we know an update has occurred to it's not calling mongo every time

        public APIService(LogService log, Config config)
        {
            Log = log;
            Config = config;

            //Mongo Connection String: mongodb://user:password@hostname:port
            Mongo = new MongoClient(String.Format("mongodb://{0}:{1}@{2}:{3}", Config.Mongo.User, Config.Mongo.Password, Config.Mongo.Hostname, Config.Mongo.Port));
            Database = Mongo.GetDatabase(config.Mongo.Database);
            GetPrefixes();

            Log.LogString("Database Service Initialized");
        }

        /// <summary>
        /// Downloads the entire server collection from Mongo and parses for just prefixes
        /// so that we don't need to search for a prefix on every damn message.
        /// </summary>
        private async void GetPrefixes()
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            List<lmaocore.Models.ServerSettings.Server> servers = (await collection.FindAsync(new BsonDocument())).ToList();
            prefixes = new Dictionary<long, string>();

            foreach(lmaocore.Models.ServerSettings.Server server in servers)
            {
                prefixes.Add(server.ServerID, server.BotSettings.CommandPrefix);
            }
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
                var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
                var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", serverID);

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
                    Log.LogString("Attempted to find prefix for " + serverID + " but none could be found!");
                    return "lmao";
                }
            }
        }

        /// <summary>
        /// Increments the usage count of a command by one
        /// </summary>
        /// <param name="command">The command to increment</param>
        public async Task UpdateUsageCount(CommandInfo command)
        {
            var collection = Database.GetCollection<lmaocore.Models.CommandUsage>("usage");
            var filter = Builders<lmaocore.Models.CommandUsage>.Filter.Eq("Command", command.Name);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                var update = Builders<lmaocore.Models.CommandUsage>.Update.Inc("Uses", 1);
                await collection.UpdateOneAsync(filter, update);
            }
            else
            {
                await collection.InsertOneAsync(new lmaocore.Models.CommandUsage()
                {
                    Command = command.Name,
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
        public async Task<lmaocore.Models.ServerSettings.Server> GetServerSettings(long serverID)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", serverID);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                lmaocore.Models.ServerSettings.Server serverSettings = await collection.Find(filter).FirstAsync();
                //Might as well update the prefix while we're at it
                if (!prefixes[serverID].Equals(serverSettings.BotSettings.CommandPrefix)) prefixes[serverID] = serverSettings.BotSettings.CommandPrefix;
                return serverSettings;
            }
            else
            {
                //Server doesn't have any settings saved. Could happen because of corrupted import.
                //For now we're just gonna return an empty one, and we'll be sure to upload it to the database
                lmaocore.Models.ServerSettings.Server serverSettings = new lmaocore.Models.ServerSettings.Server()
                {
                    ServerID = serverID,
                    BotSettings = new lmaocore.Models.ServerSettings.Settings()
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
                Log.LogString("Tried to fetch server settings from database but it did not exist: " + serverID);
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

        public async Task<int> ToggleAss(lmaocore.Models.ServerSettings.Server settings)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", settings.ServerID);

            var update = Builders<lmaocore.Models.ServerSettings.Server>.Update
                        .Set("BotSettings.ReplaceAssChance", settings.BotSettings.ReplaceAssChance == 0 ? 100 : 0)
                        .Set("BotSettings.ReactChance", settings.BotSettings.ReactChance == 0 ? 100 : 0)
                        .Set("BotSettings.LastModified", DateTime.Now);

            await collection.FindOneAndUpdateAsync(filter, update);
            return settings.BotSettings.ReplaceAssChance == 0 ? 100 : 0;
        }

        public async Task<int> SetAss(long serverID, int percent)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", serverID);

            var update = Builders<lmaocore.Models.ServerSettings.Server>.Update
                        .Set("BotSettings.ReplaceAssChance", percent)
                        .Set("BotSettings.LastModified", DateTime.Now);

            await collection.FindOneAndUpdateAsync(filter, update);
            return percent;
        }

        public async Task<int> SetReact(long serverID, int percent)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", serverID);
            var update = Builders<lmaocore.Models.ServerSettings.Server>.Update
                        .Set("BotSettings.ReactChance", percent)
                        .Set("BotSettings.LastModified", DateTime.Now);

            await collection.FindOneAndUpdateAsync(filter, update);
            return percent;
        }

        public async Task SetPrefix(long serverID, string prefix)
        {
            var collection = Database.GetCollection<lmaocore.Models.ServerSettings.Server>("servers");
            var filter = Builders<lmaocore.Models.ServerSettings.Server>.Filter.Eq("ServerID", serverID);
            var update = Builders<lmaocore.Models.ServerSettings.Server>.Update
                        .Set("BotSettings.ReactChance", percent)
                        .Set("BotSettings.LastModified", DateTime.Now);

            await collection.FindOneAndUpdateAsync(filter, update);
            return percent;
        }
    }
}

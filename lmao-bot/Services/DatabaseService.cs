using lmao_bot.Models;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Models.UserSettings;
using lmao_bot.Services.Database;
using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Diagnostics;
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
        private Dictionary<long, LmaoBotUser> users;
        private Dictionary<long, LmaoBotServer> servers;

        public Stopwatch UptimeWatch = new Stopwatch();

        private ServerSettingsCollection serverSettings;
        private UserSettingsCollection userSettings;

        public DatabaseService(BotConfig config)
        {
            Config = config;

            //Mongo Connection String: mongodb://user:password@hostname:port
            Mongo = new MongoClient(String.Format("mongodb://{0}:{1}@{2}:{3}", Config.Mongo.User, Config.Mongo.Password, Config.Mongo.Hostname, Config.Mongo.Port));
            Database = Mongo.GetDatabase(config.Mongo.Database);
            UptimeWatch.Start();

            serverSettings = new ServerSettingsCollection(Mongo, Database, this);
            userSettings = new UserSettingsCollection(Mongo, Database, this);

            users = new Dictionary<long, LmaoBotUser>();
            servers = new Dictionary<long, LmaoBotServer>();

            GetPrefixes();
        }

        /// <summary>
        /// Downloads the entire server collection from Mongo and parses for just prefixes
        /// so that we don't need to search for a prefix on every damn message.
        /// </summary>
        public async Task<Dictionary<long, string>> GetPrefixes()
        {
            var collection = Database.GetCollection<LmaoBotServer>("servers");

            List<LmaoBotServer> servers = (await collection.FindAsync(new BsonDocument())).ToList();
            prefixes = new Dictionary<long, string>();

            foreach (LmaoBotServer server in servers)
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
                var collection = Database.GetCollection<LmaoBotServer>("servers");
                var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);

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
            var collection = Database.GetCollection<CommandUsage>("usage");
            var filter = Builders<CommandUsage>.Filter.Eq("Command", command);

            if (await collection.CountDocumentsAsync(filter) == 1)
            {
                var update = Builders<CommandUsage>.Update.Inc("Uses", 1);
                await collection.UpdateOneAsync(filter, update);
            }
            else
            {
                await collection.InsertOneAsync(new CommandUsage()
                {
                    Command = command,
                    Uses = 1,
                    SubCommands = null
                });
            }
        }

        public ServerSettingsCollection GetServerSettings()
        {
            return this.serverSettings;
        }

        public UserSettingsCollection GetUserSettings()
        {
            return this.userSettings;
        }
    }
}

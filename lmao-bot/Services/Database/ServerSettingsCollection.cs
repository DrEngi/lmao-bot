using lmao_bot.Models.ServerPlaylists;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Models.UserSettings;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services.Database
{
    public class ServerSettingsCollection
    {
        private MongoClient Mongo;
        private IMongoDatabase Database;
        private IMongoCollection<LmaoBotServer> Collection;
        private DatabaseService DatabaseService;

        public ServerSettingsCollection(MongoClient mongo, IMongoDatabase database, DatabaseService databaseService)
        {
            Mongo = mongo;
            Database = database;
            DatabaseService = databaseService;
            Collection = Database.GetCollection<LmaoBotServer>("servers");
        }

        /// <summary>
        /// Create a new server settings object in the database if it doesn't already exist.
        /// </summary>
        /// <param name="serverID"></param>
        /// <returns></returns>
        public async Task CreateServerSettings(long serverID)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);

            if (await Collection.CountDocumentsAsync(filter) != 0) return;

            await Collection.InsertOneAsync(new LmaoBotServer()
            {
                ServerID = serverID,
                CustomCommands = null,
                Filters = null,
                LmaoAdmins = { },
                BotSettings = new BotSettings()
                {
                    AllowNSFW = false,
                    CommandPrefix = "lmao",
                    ReactChance = 100,
                    ReplaceAssChance = 10,
                    LastModified = DateTime.Now
                }
            });
        }

        public async Task DeleteServerSettings(long serverID)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);

            if (await Collection.CountDocumentsAsync(filter) != 0) return;

            await Collection.DeleteOneAsync(filter);
        }

        /// <summary>
        /// Retrieves the server settings for the specified ID
        /// </summary>
        /// <param name="serverID">The ID of the server</param>
        /// <returns>The specified server settings</returns>
        public async Task<LmaoBotServer> GetServerSettings(long serverID)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);

            if (await Collection.CountDocumentsAsync(filter) == 1)
            {
                LmaoBotServer serverSettings = await Collection.Find(filter).FirstAsync();
                return serverSettings;
            }
            //TODO: FOR TESTING PURPOSES ONLY.
            //this shouldn't be required if the database is up to date.
            else
            {
                await CreateServerSettings(serverID);

                LmaoBotServer serverSettings = await Collection.Find(filter).FirstAsync();
                return serverSettings;
            }
            //return null;
        }

        public async Task SetServerPrefix(long serverID, string prefix)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);
            var update = Builders<LmaoBotServer>.Update
                .Set(server => server.BotSettings.CommandPrefix, prefix)
                .Set(server => server.BotSettings.LastModified, DateTime.Now);
            await Collection.FindOneAndUpdateAsync<LmaoBotServer>(filter, update);
        }

        public async Task SetReplaceAssChance(long serverID, int chance)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);
            var update = Builders<LmaoBotServer>.Update
                .Set(server => server.BotSettings.ReplaceAssChance, chance)
                .Set(server => server.BotSettings.LastModified, DateTime.Now);
            await Collection.FindOneAndUpdateAsync<LmaoBotServer>(filter, update);
        }

        public async Task SetReactChance(long serverID, int chance)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);
            var update = Builders<LmaoBotServer>.Update
                .Set(server => server.BotSettings.ReactChance, chance)
                .Set(server => server.BotSettings.LastModified, DateTime.Now);
            await Collection.FindOneAndUpdateAsync<LmaoBotServer>(filter, update);
        }

        public async Task SetAllowNSFW(long serverID, bool allow)
        {
            var filter = Builders<LmaoBotServer>.Filter.Eq("ServerID", serverID);
            var update = Builders<LmaoBotServer>.Update
                .Set(server => server.BotSettings.AllowNSFW, allow)
                .Set(server => server.BotSettings.LastModified, DateTime.Now);
            await Collection.FindOneAndUpdateAsync<LmaoBotServer>(filter, update);
        }
    }
}

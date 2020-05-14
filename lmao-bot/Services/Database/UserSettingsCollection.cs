using lmao_bot.Models.UserSettings;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services.Database
{
    public class UserSettingsCollection
    {
        private MongoClient Mongo;
        private IMongoDatabase Database;
        private IMongoCollection<LmaoBotUser> Collection;
        private DatabaseService DatabaseService;

        public UserSettingsCollection(MongoClient mongo, IMongoDatabase database, DatabaseService databaseService)
        {
            Mongo = mongo;
            Database = database;
            Collection = Database.GetCollection<LmaoBotUser>("users");
            DatabaseService = databaseService;
        }

        /// <summary>
        /// Get the bot settings of the specified user
        /// </summary>
        /// <param name="userID">the ID of the user to get</param>
        /// <returns>The UserSettings model of the user</returns>
        public async Task<LmaoBotUser> GetUserSettings(long userID)
        {
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);

            if (await Collection.CountDocumentsAsync(filter) == 1)
            {
                LmaoBotUser settings = await Collection.Find(filter).FirstAsync();
                return settings;
            }
            else return null;
        }

        public async Task IncrementLmaoCount(long userID)
        {
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);
            var update = Builders<LmaoBotUser>.Update.Inc(settings => settings.Settings.LmaoCount, 1);
            await Collection.FindOneAndUpdateAsync(filter, update);
        }

        public async Task AddReminder(Reminder reminder, long userID)
        {
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);
            var update = Builders<LmaoBotUser>.Update.Push<Reminder>(f => f.Reminders, reminder);
            await Collection.FindOneAndUpdateAsync(filter, update);
        }

        public async Task RemoveReminder(Reminder reminder, long userID)
        {
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);
            var update = Builders<LmaoBotUser>.Update.Pull<Reminder>(f => f.Reminders, reminder);
            await Collection.FindOneAndUpdateAsync(filter, update);
        }

        public async Task<List<Reminder>> ListReminders(long userID)
        {
            return (await this.GetUserSettings(userID)).Reminders;
        }
    }
}

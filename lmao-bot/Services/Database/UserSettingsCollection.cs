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
        /// Create a new user settings object in the database if it doesn't already exist.
        /// </summary>
        /// <param name="serverID"></param>
        /// <returns></returns>
        public async Task CreateUserSettings(long userID)
        {
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);

            if (await Collection.CountDocumentsAsync(filter) != 0) return;

            await Collection.InsertOneAsync(new LmaoBotUser()
            {
                UserID = userID,
                Settings = new Settings()
                {
                    LmaoCount = 0
                },
                Reminders = new List<Reminder>()
            });
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
            else
            {
                await CreateUserSettings(userID);
                LmaoBotUser user = await Collection.Find(filter).FirstAsync();
                return user;
            }
        }

        public async Task IncrementLmaoCount(long userID)
        {
            await CreateUserSettings(userID);
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);
            var update = Builders<LmaoBotUser>.Update.Inc(settings => settings.Settings.LmaoCount, 1);
            await Collection.FindOneAndUpdateAsync(filter, update);
        }

        public async Task AddReminder(Reminder reminder, long userID)
        {
            LmaoBotUser user = await GetUserSettings(userID);
            var filter = Builders<LmaoBotUser>.Filter.Eq("UserID", userID);

            //A one-time fix for legacy users who didn't have their reminder object initialized properly.
            if (user.Reminders == null)
            {
                List<Reminder> reminders = new List<Reminder>();
                reminders.Add(reminder);
                var update = Builders<LmaoBotUser>.Update.Set(settings => settings.Reminders, reminders);
                await Collection.FindOneAndUpdateAsync(filter, update);
            }
            else
            {
                var update = Builders<LmaoBotUser>.Update.Push<Reminder>(f => f.Reminders, reminder);
                await Collection.FindOneAndUpdateAsync(filter, update);
            }
        }

        public async Task RemoveReminder(Reminder reminder, long userID)
        {
            await CreateUserSettings(userID);
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

using lmao_bot.Models;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services.Database
{
    public class BotSettingsCollection
    {
        private IMongoDatabase Database;
        private IMongoCollection<BotSetting> Collection;

        public BotSettingsCollection(IMongoDatabase database)
        {
            Database = database;
            Collection = Database.GetCollection<BotSetting>("management");
        }

        public async Task SetMaintenanceTime(DateTime time)
        {
            BotSetting newMaintSetting = new BotSetting()
            {
                SettingName = "maint",
                SettingValues = new Dictionary<string, string>()
                {
                    {"time", time.ToBinary().ToString() }
                }
            };

            var filter = Builders<BotSetting>.Filter.Eq("SettingName", "maint");
            await Collection.ReplaceOneAsync(filter, newMaintSetting, new ReplaceOptions()
            {
                IsUpsert = true
            });
        }

        public async Task<DateTime> GetMaintenanceTime()
        {
            var filter = Builders<BotSetting>.Filter.Eq("SettingName", "maint");
            BotSetting setting = (await Collection.FindAsync(filter)).FirstOrDefault();

            if (setting != null) return new DateTime(Convert.ToInt64(setting.SettingValues["time"]));
            else return DateTime.UnixEpoch;
        }

        public async Task AddToBlacklist(long userID)
        {
            var filter = Builders<BotSetting>.Filter.Eq("SettingName", "blacklist");

            if (await Collection.CountDocumentsAsync(filter) == 0)
            {
                BotSetting newBlacklistSetting = new BotSetting()
                {
                    SettingName = "blacklist",
                    BlacklistedUsers = new List<long>()
                    {
                        userID
                    }
                };
                await Collection.InsertOneAsync(newBlacklistSetting);
            }
            else
            {
                var update = Builders<BotSetting>.Update.Push("BlacklistedUsers", userID);
                await Collection.UpdateOneAsync(filter, update);
            }
        }

        public async Task<List<long>> GetBlacklist()
        {
            var filter = Builders<BotSetting>.Filter.Eq("SettingName", "blacklist");
            BotSetting setting = (await Collection.FindAsync(filter)).FirstOrDefault();

            if (setting != null)
            {
                return setting.BlacklistedUsers;
            }
            else return new List<long>();
        }
    }
}

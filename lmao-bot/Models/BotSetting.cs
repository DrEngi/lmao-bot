using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Models
{
    public class BotSetting
    {
        public ObjectId _id { get; set; }
        public string SettingName { get; set; }
        [BsonIgnoreIfNull]
        public Dictionary<string, string> SettingValues { get; set; }
        [BsonIgnoreIfNull]
        public List<long> BlacklistedUsers { get; set; }
    }
}

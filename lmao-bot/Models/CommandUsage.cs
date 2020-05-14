using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Models
{
    public class CommandUsage
    {
        public ObjectId _id { get; set; }
        public string Command { get; set; }
        public int Uses { get; set; }
        public Dictionary<string, int> SubCommands { get; set; }
    }
}

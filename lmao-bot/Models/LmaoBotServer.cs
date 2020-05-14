﻿using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Models.ServerSettings
{
    //ServerSettings Object for Mongo
    //Also contains lmao admins
    public class LmaoBotServer
    {
        public ObjectId _id { get; set; }
        public Int64 ServerID { get; set; }
        public BotSettings BotSettings { get; set; }
        public List<string> LmaoAdmins { get; set; }
        public Dictionary<string, Filter> Filters { get; set; }
        public Dictionary<string, CustomCommand> CustomCommands { get; set; }
    }

    public class BotSettings
    {
        public string CommandPrefix { get; set; }
        public int ReplaceAssChance { get; set; }
        public int ReactChance { get; set; }
        public bool AllowNSFW { get; set; }
        public DateTime LastModified { get; set; }
    }

    public class Filter
    {
        public string Activator { get; set; }
        public string Response { get; set; }
        public string[] Flags { get; set; }
    }

    public class CustomCommand
    {
        public string Activator { get; set; }
        public string Response { get; set; }
    }
}

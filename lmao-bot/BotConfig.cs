﻿using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot
{
    public class BotConfig
    {
        public string Token { get; set; }
        public string Dbl { get; set; }
        public MongoConfig Mongo { get; set; }
        public LavalinkConfig Lavalink { get; set; }
    }

    public class MongoConfig
    {
        public string Hostname { get; set; }
        public int Port { get; set; }
        public string User { get; set; }
        public string Password { get; set; }
        public string Database { get; set; }
    }

    public class LavalinkConfig
    {
        public string Hostname { get; set; }
        public int Port { get; set; }
        public string Region { get; set; }
        public string Password { get; set; }
        public string Name { get; set; }
    }
}

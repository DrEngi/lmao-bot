using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Models
{
    class Config
    {
        public string Token { get; set; }
        public string Dbl { get; set; }
        public MongoConfig Mongo { get; set; }
        public LavalinkConfig Lavalink { get; set; }
    }

    class MongoConfig
    {
        public string Hostname { get; set; }
        public int Port { get; set; }
        public string User { get; set; }
        public string Password { get; set; }
        public string Database { get; set; }
    }

    class LavalinkConfig
    {
        public string Hostname { get; set; }
        public int Port { get; set; }
        public string Region { get; set; }
        public string Password { get; set; }
        public string Name { get; set; }
    }
}

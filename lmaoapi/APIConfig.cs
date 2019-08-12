using System;
using System.Collections.Generic;
using System.Text;

namespace lmaocore
{
    public class Config
    {
        public string lmaoauthkey { get; set; }
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

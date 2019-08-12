using System;
using System.Collections.Generic;
using System.Text;

namespace lmaocore
{
    public class Config
    {
        public string Token { get; set; }
        public string Dbl { get; set; }
        public API Api { get; set; }
        public LavalinkConfig Lavalink { get; set; }
    }

    public class API
    {
        public string URL { get; set; }
        public int Port { get; set; }
        public string AuthKey { get; set; }
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

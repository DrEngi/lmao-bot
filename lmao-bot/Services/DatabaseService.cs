using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Services
{
    public class DatabaseService
    {
        private readonly LogService Log;

        public DatabaseService(LogService log)
        {
            Log = log;
            Log.LogString("Database Service Initialized");
        }

        public void test()
        {
            Log.LogString("testtest");
        }
    }
}

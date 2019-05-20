﻿using lmao_bot.Models;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Services
{
    public class DatabaseService
    {
        private readonly LogService Log;
        private readonly Config Config;

        private MongoClient Mongo;
        private IMongoDatabase Database;

        public DatabaseService(LogService log, Config config)
        {
            Log = log;
            Config = config;

            //Mongo Connection String: mongodb://user:password@hostname:port
            Mongo = new MongoClient(String.Format("mongodb://{0}:{1}@{2}:{3}", Config.Mongo.User, Config.Mongo.Password, Config.Mongo.Hostname, Config.Mongo.Port));
            Database = Mongo.GetDatabase(config.Mongo.Database);

            Log.LogString("Database Service Initialized");
        }
    }
}

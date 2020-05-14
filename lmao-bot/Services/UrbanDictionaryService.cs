using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using UrbanDictionnet;

namespace lmao_bot.Services
{
    public class UrbanDictionaryService
    {
        UrbanClient Client;

        public UrbanDictionaryService()
        {
            Client = new UrbanClient();
        }

        public async Task<WordDefine> Define(string word)
        {
            return await Client.GetWordAsync(word);
        }

        public async Task<UniqueWordDefine> DefineID(int id)
        {
            return await Client.GetWordAsync(id);
        }

        public async Task<DefinitionData> DefineRandom()
        {
            return await Client.GetRandomWordAsync();
        }
    }
}

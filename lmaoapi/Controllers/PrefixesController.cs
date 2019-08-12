using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace lmaoapi.Controllers
{
    /// <summary>
    /// I'm separating out prefixes because they'll get a lot of traffic.
    /// </summary>
    [Route("api/[controller]")]
    [ApiController]
    public class PrefixesController : ControllerBase
    {
        // GET: api/Prefixes
        [HttpGet]
        public IEnumerable<string> Get()
        {
            return new string[] { "value1", "value2" };
        }

        // GET: api/Prefixes/5
        [HttpGet("{id}", Name = "Get")]
        public string Get(int id)
        {
            return "value";
        }

        // POST: api/Prefixes
        [HttpPost]
        public void Post([FromBody] string value)
        {
        }

        // PUT: api/Prefixes/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE: api/ApiWithActions/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}

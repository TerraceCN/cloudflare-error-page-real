# Cloudflare Error Page Real

Create a Cloudflare error page with real-time edge location data.

The error page template is from [donlon/cloudflare-error-page](https://github.com/donlon/cloudflare-error-page).


## How to use

```bash
docker run -d \
  --name cf-error-page-real \
  -p 8000:8000 \
  ghcr.io/terracecn/cf-error-page-real:latest
```


## Customization

### 1. Update IATA Code List
The entry-point datacenter location is determined using the 3-letter IATA code suffix from the `CF-Ray` header. You can customize the location mapping by replacing the `/app/iata.json` file.

**Example `iata.json` structure**:
```json
{
  "NRT": "Tokyo, Japan",
  "LAX": "Los Angeles, USA",
  "LHR": "London, UK",
  "...": "..."
}
```

**Mount custom IATA file**:
```bash
-v /path/to/your/iata.json:/app/iata.json
```


### 2. Modify Error Page Configuration
Customize the error page appearance and behavior by overriding the `/app/config.json` file. The configuration format is fully compatible with the original project's [configuration editor](https://virt.moe/cloudflare-error-page/editor/).

**Example `config.json`**:
```json
{
  "title": "Internal server error",
  "error_code": "500",
  "more_information": {
      "hidden": false,
      "text": "cloudflare.com",
      "link": "",
      "for": "more information"
  },
  "...": "..."
}
```

**Mount custom config file**:
```bash
-v /path/to/your/config.json:/app/config.json
```


## Why not use Cloudflare Worker?

Cloudflare Workers cannot directly resolve the physical location of the entry-point datacenter using the `CF-Ray` header. This project decodes the IATA code from `CF-Ray` to provide accurate edge location information.


## License

This project is based on [donlon/cloudflare-error-page](https://github.com/donlon/cloudflare-error-page) (MIT License). Modifications are released under the same license.
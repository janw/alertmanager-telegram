# Alertmanager Telegram relay

A simple webhook notification relay for Prometheus Alertmanager.

## Running with Docker

First, you'll need two environment variables:

* `TELEGRAM_CHAT_ID`: Your Telegram user ID. Retrieve it from [@userinfobot](https://t.me/userinfobot).
* `TELEGRAM_TOKEN`: An API token for a bot you created to send you the alert messages. Create one via [@botfather](https://t.me/botfather).

Next, provide the variables to the docker container:

```bash
docker run \
    --name alertmanager-telegram \
    -e TELEGRAM_CHAT_ID="..." \
    -e TELEGRAM_TOKEN="..." \
    -p 8080:8080 \
    janwh/alertmanager-telegram
```

Finally, in the Alertmanager config, add the relay as a webhook receiver:

```yaml
receivers:
  - name: "telegram"
    webhook_configs:
      - url: "http://alertmanager-telegram:8080/alerts"
        send_resolved: true
```

## Templating

A custom alert template can be added by overriding `/templates/default.html`:

```bash
docker run \
    --name alertmanager-telegram \
    -e TELEGRAM_CHAT_ID="..." \
    -e TELEGRAM_TOKEN="..." \
    -v /path/to/my/template.html:/templates/default.html \
    -p 8080:8080 \
    janwh/alertmanager-telegram
```

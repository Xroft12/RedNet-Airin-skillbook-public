# Airin Signal Sensor

Публичный прототип пассивного нейросенсора Айрин.

Это не firewall, не VPN-переключатель и не live-сетевой агент. Прототип читает только replay-файлы JSONL, сохраняет обезличенные признаки в SQLite и выдает оценку состояния в режиме `observe`.

## Что хранится

- тип события;
- протокол;
- порт;
- направление;
- размеры и длительность;
- DNS/TLS/TCP reset-симптомы;
- хеши адресов/имен вместо исходных значений;
- оценка `ok`, `degraded`, `suspicious`, `unknown`, `noise`;
- рекомендация Guardian без исполнения.

## Что не хранится

- payload;
- текст сообщений;
- cookies;
- токены;
- OAuth/Telegram-сессии;
- приватные ключи;
- исходные IP/hostnames в открытом виде.

## Быстрый запуск

```powershell
python sensor-prototype\airin-signal-sensor\sensor.py init --state-dir tmp\sensor-demo
python sensor-prototype\airin-signal-sensor\sensor.py ingest --state-dir tmp\sensor-demo --replay sensor-prototype\airin-signal-sensor\samples\normal-flow.jsonl
python sensor-prototype\airin-signal-sensor\sensor.py assess --state-dir tmp\sensor-demo
python -m unittest discover sensor-prototype\airin-signal-sensor\tests
```

## Следующий этап

Live Zeek/Suricata подключаются отдельным окном обслуживания. Этот прототип нужен, чтобы проверить механику признаков, памяти попыток и рекомендаций без риска для рабочей сети.

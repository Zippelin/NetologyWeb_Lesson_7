## Запуск

```docker-compose up -d --build```

#### В ряде случаев под виндой может потребоваться:
```sysctl net.ipv4.conf.all.forwarding=1```

```sudo iptables -P FORWARD ACCEPT```

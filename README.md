# MQTT-Panel

一个使用MQTT协议的数据展示面板。

用于对接下位机。

## 技术栈

Vite+Vue3+EChart.js+TypeScript

## 构建&部署

```bash
# 前端
pnpm i && vite build
# 后端
go mod tidy && go build
```

构建完成后，直接启动`mqtt-server`即可。

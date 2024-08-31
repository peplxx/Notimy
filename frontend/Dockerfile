# Указываем базовый образ
FROM node:18-alpine
#  AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json в контейнер
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь код в контейнер
COPY . .

# Строим приложение
RUN npm run build

# # Указываем базовый образ для запуска
# FROM node:18-alpine AS runner

# # Устанавливаем рабочую директорию
# WORKDIR /app

# # Копируем файлы из стадии сборки
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package*.json ./

# Указываем порт, который будет прослушиваться приложением
EXPOSE 3000

# Запускаем приложение
#ARG HTTPS=true
CMD ["npm", "run", "start"]

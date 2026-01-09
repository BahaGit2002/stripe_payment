# Django + Stripe Payment Integration

Проект для интеграции платежной системы Stripe с Django. Реализованы основные функции и все бонусные задачи.

## Функционал

### Основные возможности:
- ✅ Django модель `Item` с полями (name, description, price, currency)
- ✅ API метод `GET /buy/{id}` - получение Stripe Session Id для оплаты товара
- ✅ API метод `GET /item/{id}` - HTML страница с информацией о товаре и кнопкой Buy
- ✅ Интеграция с Stripe Checkout

### Бонусные задачи:
- ✅ Docker и Docker Compose для запуска
- ✅ Использование environment variables для конфигурации
- ✅ Django Admin панель для управления моделями
- ✅ Модель `Order` для объединения нескольких товаров
- ✅ Модели `Discount` и `Tax` с интеграцией в Stripe Checkout
- ✅ Поддержка нескольких валют (USD, EUR) с разными Stripe ключами
- ✅ Реализация Stripe Payment Intent (альтернатива Session)

## Установка и запуск

### Локальный запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/BahaGit2002/stripe_payment.git
cd stripe_payment
```

2. **Создайте виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте environment variables:**
```bash
cp env.example .env
# Отредактируйте .env файл и добавьте ваши Stripe ключи
```

5. **Выполните миграции:**
```bash
python manage.py migrate
```

6. **Создайте суперпользователя для доступа к админке:**
```bash
python manage.py createsuperuser
```
7. **Для быстрого доступа к административной панели выполните:**

```bash
python manage.py create_admin
```

Команда автоматически создаст администратора со следующими учётными данными:
- username: admin
- email:    admin@example.com
- password: admin

8. **Запустите сервер:**
```bash
python manage.py runserver
```

### Запуск с Docker

1. **Создайте .env файл:**
```bash
cp env.example .env
# Отредактируйте .env файл
```

2. **Запустите с Docker Compose:**
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## Настройка Stripe

1. Зарегистрируйтесь на [stripe.com](https://stripe.com)
2. Получите тестовые ключи в Dashboard → Developers → API keys
3. Для поддержки нескольких валют создайте отдельные аккаунты или используйте разные ключи
4. Добавьте ключи в `.env` файл:
   - `STRIPE_SECRET_KEY` - секретный ключ
   - `STRIPE_PUBLISHABLE_KEY` - публичный ключ

## Использование

### API Endpoints

#### Получить HTML страницу товара
```bash
curl http://localhost:8000/item/1/
```

#### Создать Stripe Session для оплаты товара
```bash
curl http://localhost:8000/buy/1/
```

Ответ:
```json
{"id": "cs_test_..."}
```

#### Создать Stripe Session для оплаты заказа
```bash
curl http://localhost:8000/order/1/
```

#### Создать Payment Intent (бонус)
```bash
curl http://localhost:8000/payment-intent/1/
```

### Django Admin

Доступ к админ-панели: http://localhost:8000/admin/

В админ-панели можно:
- Создавать и редактировать товары (Items)
- Создавать заказы (Orders) с несколькими товарами
- Настраивать скидки (Discounts) и налоги (Taxes)
- Управлять всеми моделями

### Создание скидок и налогов в Stripe

Для работы скидок и налогов необходимо:

1. **Создать Coupon в Stripe:**
   - Перейдите в Stripe Dashboard → Products → Coupons
   - Создайте купон с нужным процентом
   - Скопируйте ID купона и добавьте в поле `stripe_coupon_id` модели Discount

2. **Создать Tax Rate в Stripe:**
   - Перейдите в Stripe Dashboard → Products → Tax rates
   - Создайте налоговую ставку
   - Скопируйте ID и добавьте в поле `stripe_tax_rate_id` модели Tax

## Структура проекта

```
stripe_payment/
├── payments/              # Приложение для платежей
│   ├── management/
│   │   └── commands/
│   │       └── create_superuser.py
│   ├── models.py         # Модели: Item, Order, Discount, Tax
│   ├── views.py          # Представления для API
│   ├── urls.py           # URL маршруты
│   └── admin.py          # Настройка админ-панели
├── templates/            # HTML шаблоны
│   └── payments/
│       └── item_detail.html
├── core/                # Настройки проекта
│   ├── settings.py      # Настройки Django
│   └── urls.py          # Главный URL конфиг
├── Dockerfile           # Docker образ
├── docker-compose.yml   # Docker Compose конфигурация
├── requirements.txt     # Python зависимости
└── README.md           # Документация
```

## Модели

### Item
- `name` - название товара
- `description` - описание
- `price` - цена
- `currency` - валюта (USD/EUR)

### Order
- `items` - множество товаров
- `discount` - скидка (опционально)
- `tax` - налог (опционально)
- `created_at` - дата создания

### Discount
- `name` - название скидки
- `percent_off` - процент скидки
- `stripe_coupon_id` - ID купона в Stripe

### Tax
- `name` - название налога
- `percentage` - процент налога
- `stripe_tax_rate_id` - ID налоговой ставки в Stripe

## Тестирование

1. Создайте товар через админ-панель
2. Откройте http://localhost:8000/item/1/
3. Нажмите кнопку "Buy"
4. Будет выполнен редирект на Stripe Checkout
5. Используйте тестовую карту: `4242 4242 4242 4242`

## Развертывание на сервере

Для развертывания на удаленном сервере:

1. Установите зависимости сервера (nginx, gunicorn и т.д.)
2. Настройте `.env` файл с production ключами
3. Установите `DEBUG=False` в `.env`
4. Добавьте домен в `ALLOWED_HOSTS`
5. Настройте статические файлы
6. Используйте `gunicorn` или другой WSGI сервер

Пример с gunicorn:
```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

# Petsy — техническая спецификация и структура кода

## 1. Цели платформы

**Petsy** — единая платформа для владельцев питомцев, специалистов и бизнесов (ветклиники, груминг, гостиницы, приюты, заводчики), объединяющая:
- поиск и бронирование услуг;
- онлайн-консультации;
- работу с контентом (статьи);
- управление заявками на питомцев;
- CRM-кабинеты для бизнес-партнёров;
- централизованные платежи, отзывы, чаты и модерацию.

---

## 2. Рекомендуемый стек технологий

### Frontend
- **Next.js 14 (App Router) + TypeScript**
- **UI**: Tailwind CSS + shadcn/ui
- **State / Data fetching**: React Query + Zustand
- **Forms**: React Hook Form + Zod
- **Карты**: Mapbox GL JS (или Яндекс Карты для RU рынка)
- **Realtime**: WebSocket (Socket.IO client) для чатов и live-статусов
- **Видео**: WebRTC через Daily/Twilio SDK

### Backend
- **NestJS + TypeScript** (модульная архитектура)
- **ORM**: Prisma
- **Auth**: JWT (access + refresh), OAuth2 (Google/Apple), optional 2FA
- **Queue**: BullMQ + Redis (уведомления, счета, webhooks, модерация)
- **Realtime**: Socket.IO Gateway
- **Storage**: S3-совместимое хранилище (аватары, документы, медиа)

### База данных и инфраструктура
- **PostgreSQL 16** (основная БД)
- **Redis** (кеш, rate-limit, сессии, pub/sub)
- **Elasticsearch/OpenSearch** (поиск по услугам/статьям/специалистам)
- **Payments**: Stripe / ЮKassa / CloudPayments
- **Observability**: OpenTelemetry + Prometheus + Grafana + Sentry
- **Deploy**: Docker + Kubernetes (или ECS), CI/CD на GitHub Actions

---

## 3. Архитектура приложения

## 3.1 Логическая схема

- **Web App (Next.js)**
- **API Gateway (NestJS)**
- Доменные модули:
  - Auth & Users
  - Pets
  - Booking (ветклиника/груминг/гостиница/специалисты)
  - Consultations
  - Adoption
  - Reviews
  - Articles
  - Payments
  - Chat/Calls
  - CRM
  - Admin/Moderation
- Внешние интеграции:
  - Maps
  - Video provider
  - Payment provider
  - Notifications (email/SMS/push)

## 3.2 Модульный монолит → микросервисы

Старт: **модульный монолит** (быстрее time-to-market).
Рост: выделить сервисы:
- Payments Service
- Realtime Service
- Search Service
- Notification Service

---

## 4. Роли пользователей и RBAC

## 4.1 Роли
1. **Обычный пользователь (PET_OWNER)**
2. **Специалист (SPECIALIST)**
3. **Бизнес-аккаунт**:
   - VET_CLINIC
   - GROOMING_SALON
   - PET_HOTEL
   - SERVICE_AGGREGATOR
4. **Приют/Заводчик**:
   - SHELTER
   - BREEDER
5. **Администратор (ADMIN)**
6. **Старший технический специалист (SUPER_ADMIN / TECH_LEAD)** — полный доступ, включая системные настройки и аудит.

## 4.2 Принципы доступа
- RBAC + policy-based guards (например, пользователь может редактировать только свои записи).
- Обязательная проверка `resource_owner_id`.
- Soft-delete и audit-log для критичных сущностей.
- Разделение прав на чтение/изменение/модерацию/финансы.

---

## 5. Основные пользовательские сценарии (по разделам)

## 5.1 Главная страница
### Верхнее меню
- Логотип
- Статьи
- О нас
- Контакты
- Вход
- Регистрация

### Основные сервисные блоки
- Запись в ветклинику
- Консультация с ветеринаром
- Запись на груминг
- Бронирование зоогостиницы
- Поиск специалистов
- Приютить питомца

### Партнёрские CTA-блоки
- Стать специалистом
- Для бизнеса
- Для заводчиков и приютов

## 5.2 Личный кабинет
- Профиль + редактирование
- Управление питомцами
- Активные/прошлые записи
- Отзывы по услугам
- Онлайн-консультации (видеозвонок/чат/звонок)
- Избранные статьи

## 5.3 Ветклиники
- Каталог клиник с фильтрами/сортировками
- Карта
- Страница клиники
- Слоты и онлайн-запись

## 5.4 Консультации
- Каталог врачей
- Профиль врача + тип консультации (video/chat/call)
- Инвойс/оплата консультации

## 5.5 Груминг
- Каталог салонов + карта
- Услуги/цены
- Запись и оплата

## 5.6 Зоогостиница
- Фильтры по городу/датам/типу питомца
- Карточки гостиниц + карта
- Бронирование размещения

## 5.7 Специалисты
- Категории: сиделка, выгульщик, кинолог
- Профиль специалиста: услуги, цены, отзывы
- Бронирование + оплата + чат

## 5.8 Приютить питомца
- Категории: Из приюта / От заводчика
- Страница питомца
- Заявка, оплата (опционально), подтверждение передачи

## 5.9 Статьи
- Поиск
- Категории
- Избранное

---

## 6. CRM для бизнес-аккаунтов

## 6.1 Общие CRM-модули
- Дашборд метрик (заявки, конверсия, выручка)
- Управление услугами и прайсом
- Управление расписанием и слотами
- Управление заявками/бронированиями
- Отзывы и ответы
- Чат с клиентами
- Финансы: оплаты, комиссии, вывод средств
- Документы и верификация

## 6.2 По типам
- **Ветклиника**: врачи, кабинеты, услуги, графики, мед.карточки
- **Ветеринар**: консультации, слоты, тарифы, история обращений
- **Груминг**: пакеты услуг, длительность, мастера
- **Зоогостиница**: номерной фонд, лимиты, сезонные тарифы
- **Специалисты**: география выездов, длительность визита
- **Приют/заводчик**: карточки питомцев, статус передачи, документы
- **Администраторы**: глобальная модерация, споры, возвраты

## 6.3 Финансовые операции
- Сплит-платежи (платформа + исполнитель)
- Статусы: `pending`, `authorized`, `captured`, `refunded`, `payout_pending`, `payout_done`
- Отложенные выплаты с удержанием на период споров

---

## 7. Модели данных (PostgreSQL + Prisma)

Ниже минимальный набор ключевых сущностей:
- User
- Pet
- Business
- SpecialistProfile
- Service
- Booking
- Review
- Article
- FavoriteArticle
- ConsultationSession
- Invoice/Payment
- AdoptionPet
- AdoptionRequest
- ChatRoom/Message

### Пример Prisma schema (фрагмент)
```prisma
enum Role {
  PET_OWNER
  SPECIALIST
  BUSINESS
  SHELTER
  BREEDER
  ADMIN
  SUPER_ADMIN
}

enum BookingType {
  VET_CLINIC
  CONSULTATION
  GROOMING
  HOTEL
  SPECIALIST
}

enum BookingStatus {
  PENDING
  CONFIRMED
  COMPLETED
  CANCELED
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  phone         String?   @unique
  passwordHash  String
  role          Role      @default(PET_OWNER)
  fullName      String
  createdAt     DateTime  @default(now())
  pets          Pet[]
  reviews       Review[]
  bookings      Booking[]
}

model Pet {
  id            String   @id @default(cuid())
  ownerId       String
  owner         User     @relation(fields: [ownerId], references: [id])
  name          String
  species       String
  breed         String?
  birthDate     DateTime?
  weightKg      Float?
  medicalNotes  String?
}

model Service {
  id            String   @id @default(cuid())
  providerId    String
  type          BookingType
  title         String
  description   String?
  durationMin   Int
  priceCents    Int
  isActive      Boolean  @default(true)
  createdAt     DateTime @default(now())
}

model Booking {
  id            String        @id @default(cuid())
  userId        String
  petId         String?
  serviceId     String
  type          BookingType
  startAt       DateTime
  endAt         DateTime
  status        BookingStatus @default(PENDING)
  totalCents    Int
  notes         String?
  createdAt     DateTime      @default(now())

  user          User          @relation(fields: [userId], references: [id])
  pet           Pet?          @relation(fields: [petId], references: [id])
}

model Review {
  id            String   @id @default(cuid())
  userId        String
  serviceId     String
  bookingId     String?
  rating        Int
  comment       String?
  createdAt     DateTime @default(now())

  user          User     @relation(fields: [userId], references: [id])
}
```

---

## 8. REST API (пример структуры)

## 8.1 Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

## 8.2 Users/Pets
- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `POST /api/v1/pets`
- `GET /api/v1/pets`
- `PATCH /api/v1/pets/:id`
- `DELETE /api/v1/pets/:id`

## 8.3 Services
- `GET /api/v1/services`
- `POST /api/v1/services`
- `PATCH /api/v1/services/:id`
- `DELETE /api/v1/services/:id`

## 8.4 Bookings
- `GET /api/v1/bookings?status=active`
- `POST /api/v1/bookings`
- `PATCH /api/v1/bookings/:id/cancel`

## 8.5 Reviews
- `POST /api/v1/reviews`
- `GET /api/v1/services/:id/reviews`

## 8.6 Articles
- `GET /api/v1/articles`
- `GET /api/v1/articles/:slug`
- `POST /api/v1/articles/:id/favorite`
- `DELETE /api/v1/articles/:id/favorite`

## 8.7 Adoption
- `GET /api/v1/adoption/pets`
- `GET /api/v1/adoption/pets/:id`
- `POST /api/v1/adoption/requests`
- `PATCH /api/v1/adoption/requests/:id/status`

## 8.8 CRM
- `GET /api/v1/crm/dashboard`
- `GET /api/v1/crm/bookings`
- `PATCH /api/v1/crm/bookings/:id/status`
- `GET /api/v1/crm/finance/transactions`
- `POST /api/v1/crm/finance/payouts`

---

## 9. Frontend routes (Next.js App Router)

```txt
/
/articles
/articles/[slug]
/about
/contacts
/auth/login
/auth/register
/cabinet
/cabinet/profile
/cabinet/pets
/cabinet/bookings
/cabinet/reviews
/cabinet/consultations
/vet-clinics
/vet-clinics/[id]
/consultations
/consultations/[vetId]
/grooming
/grooming/[id]
/hotels
/hotels/[id]
/specialists
/specialists/[id]
/adoption
/adoption/[petId]
/crm
/crm/services
/crm/bookings
/crm/reviews
/crm/finance
/admin
```

---

## 10. Бизнес-логика и ключевые правила

1. **Онлайн-запись**
   - Нельзя забронировать занятый слот.
   - Проверка совместимости услуги и типа питомца.
   - Таймаут на оплату брони (например, 15 минут).

2. **Отзывы**
   - Отзыв можно оставить только после завершённой записи.
   - Один booking → один отзыв.

3. **Консультации**
   - Сессия активируется только после успешной оплаты.
   - Генерация временной комнаты видео/чата.

4. **Adoption flow**
   - Статусы: `new -> review -> approved/rejected -> transferred`.
   - Подписание акта передачи (e-sign или подтверждение кодом).

5. **Модерация**
   - Жалобы, фрод-сигналы, ручная проверка.
   - Право блокировки контента/аккаунтов у ADMIN/SUPER_ADMIN.

---

## 11. Минимальная реализация: backend (NestJS)

## 11.1 DTO: регистрация/логин
```ts
// auth/dto/register.dto.ts
import { IsEmail, IsString, MinLength } from 'class-validator';

export class RegisterDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(8)
  password!: string;

  @IsString()
  fullName!: string;
}
```

```ts
// auth/auth.controller.ts
import { Body, Controller, Post } from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto } from './dto/register.dto';

@Controller('api/v1/auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  @Post('login')
  login(@Body() dto: { email: string; password: string }) {
    return this.authService.login(dto.email, dto.password);
  }
}
```

## 11.2 CRUD для услуг
```ts
// services/services.controller.ts
import { Body, Controller, Delete, Get, Param, Patch, Post, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt.guard';
import { RolesGuard } from '../auth/roles.guard';
import { Roles } from '../auth/roles.decorator';
import { ServicesService } from './services.service';

@Controller('api/v1/services')
export class ServicesController {
  constructor(private readonly servicesService: ServicesService) {}

  @Get()
  list() {
    return this.servicesService.listPublic();
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('SPECIALIST', 'BUSINESS', 'SHELTER', 'BREEDER', 'SUPER_ADMIN')
  @Post()
  create(@Body() dto: any) {
    return this.servicesService.create(dto);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('SPECIALIST', 'BUSINESS', 'SUPER_ADMIN')
  @Patch(':id')
  update(@Param('id') id: string, @Body() dto: any) {
    return this.servicesService.update(id, dto);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('SPECIALIST', 'BUSINESS', 'SUPER_ADMIN')
  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.servicesService.remove(id);
  }
}
```

## 11.3 Онлайн-запись
```ts
// bookings/bookings.service.ts
async createBooking(dto: {
  userId: string;
  petId?: string;
  serviceId: string;
  startAt: Date;
}) {
  const service = await this.prisma.service.findUniqueOrThrow({ where: { id: dto.serviceId } });
  const endAt = new Date(dto.startAt.getTime() + service.durationMin * 60 * 1000);

  const overlap = await this.prisma.booking.findFirst({
    where: {
      serviceId: dto.serviceId,
      status: { in: ['PENDING', 'CONFIRMED'] },
      AND: [{ startAt: { lt: endAt } }, { endAt: { gt: dto.startAt } }],
    },
  });

  if (overlap) throw new Error('Slot is not available');

  return this.prisma.booking.create({
    data: {
      userId: dto.userId,
      petId: dto.petId,
      serviceId: dto.serviceId,
      type: service.type,
      startAt: dto.startAt,
      endAt,
      totalCents: service.priceCents,
      status: 'PENDING',
    },
  });
}
```

## 11.4 Отзывы
```ts
// reviews/reviews.service.ts
async createReview(userId: string, dto: { bookingId: string; serviceId: string; rating: number; comment?: string }) {
  const booking = await this.prisma.booking.findUniqueOrThrow({ where: { id: dto.bookingId } });
  if (booking.userId !== userId) throw new Error('Forbidden');
  if (booking.status !== 'COMPLETED') throw new Error('Booking not completed');

  const exists = await this.prisma.review.findFirst({ where: { bookingId: dto.bookingId } });
  if (exists) throw new Error('Review already exists');

  return this.prisma.review.create({
    data: {
      userId,
      bookingId: dto.bookingId,
      serviceId: dto.serviceId,
      rating: dto.rating,
      comment: dto.comment,
    },
  });
}
```

---

## 12. Минимальная реализация: frontend (Next.js)

## 12.1 Форма логина/регистрации
```tsx
// app/auth/login/page.tsx
'use client';

import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormData = z.infer<typeof schema>;

export default function LoginPage() {
  const { register, handleSubmit } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3 max-w-md">
      <input {...register('email')} placeholder="Email" className="input" />
      <input {...register('password')} placeholder="Пароль" type="password" className="input" />
      <button type="submit" className="btn-primary">Войти</button>
    </form>
  );
}
```

## 12.2 Компонент карточки услуги
```tsx
// components/service-card.tsx
type ServiceCardProps = {
  title: string;
  priceCents: number;
  durationMin: number;
  rating?: number;
};

export function ServiceCard({ title, priceCents, durationMin, rating }: ServiceCardProps) {
  return (
    <article className="rounded-2xl border p-4">
      <h3 className="font-semibold text-lg">{title}</h3>
      <p>Цена: {(priceCents / 100).toFixed(2)} ₽</p>
      <p>Длительность: {durationMin} мин.</p>
      <p>Рейтинг: {rating ?? '—'}</p>
      <button className="btn-primary mt-3">Записаться</button>
    </article>
  );
}
```

## 12.3 Страница списка услуг + бронирование
```tsx
// app/vet-clinics/page.tsx
import { ServiceCard } from '@/components/service-card';

async function getServices() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/services?type=VET_CLINIC`, { cache: 'no-store' });
  return res.json();
}

export default async function VetClinicsPage() {
  const services = await getServices();

  return (
    <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {services.items.map((s: any) => (
        <ServiceCard
          key={s.id}
          title={s.title}
          priceCents={s.priceCents}
          durationMin={s.durationMin}
          rating={s.rating}
        />
      ))}
    </section>
  );
}
```

---

## 13. Нефункциональные требования

- SLA API: 99.9%
- P95 latency для ключевых `GET`: < 300ms
- Безопасность: OWASP ASVS, rate limit, CSRF protection, WAF
- Шифрование: TLS 1.2+, шифрование персональных данных в покое
- Логи: централизованный аудит действий админов и операций выплат
- Соответствие требованиям персональных данных (GDPR/локальные нормы)

---

## 14. План релизов

### MVP (8–12 недель)
- Auth + профиль + питомцы
- Каталоги услуг + карточки
- Бронирование и базовая оплата
- Отзывы
- Статьи + избранное
- Простой CRM для партнёров

### Phase 2
- Онлайн-консультации (видео)
- Adoption workflow
- Расширенная аналитика CRM
- Модерация и dispute-center

### Phase 3
- Рекомендательная система
- ML scoring для фрода и качества лидов
- Мобильные приложения (React Native/Flutter)

---

## 15. Краткий вывод

Предложенный стек (Next.js + NestJS + PostgreSQL + Prisma + Redis) закрывает все заявленные сценарии Petsy, оставаясь масштабируемым и удобным для поэтапного развития от MVP до высоконагруженной multi-role платформы с CRM, платежами, онлайн-консультациями и модерацией.

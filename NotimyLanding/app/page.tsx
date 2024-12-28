import {title} from "@/components/primitives";
import {siteConfig} from "@/config/site";
import {Link} from "@nextui-org/link";
import Image from 'next/image';

export default function AboutPage() {
  return (
    <div className="font-sans text-gray-900 flex flex-col gap-9">

      {/* Hero Section */}
      <section id="hero" className="bg-blue-50 py-16 rounded-2xl drop-shadow-xl">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl font-bold text-blue-600 mb-4">
            Упростите управление очередями с Notimy
          </h1>
          <p className="text-lg text-gray-700 mb-8">
            Открывайте удобные каналы, где клиенты отслеживают заказы в реальном времени.<br/> Всё без скачивания
            приложения — просто в браузере.
          </p>
          <Link href={siteConfig.links.telegram}>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-blue-700">
              Присоединиться
            </button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="features">
        <div className="flex p-3">
          <div className="flex-1 flex flex-col justify-center">
            <div className="text-3xl font-semibold text-center mb-8">Современный интерфейс</div>
            <div className="text-3xl font-semibold text-center mb-8">Лёгкое управление</div>
            <div className="text-3xl font-semibold text-center mb-8">Максимальная прозрачность</div>
            <div className="text-3xl font-semibold text-center mb-8">Увеличение эффективности</div>
          </div>
          <Image
            src="/notimy phone.png"
            alt="Example Image"
            width={500}
            height={400}
            className=""
          />
        </div>
      </section>

      {/* About Section */}
      <section className="py-16">
        <div className="container mx-auto text-center drop-shadow-xl">
          <h2 className="text-3xl font-semibold text-center mb-8">
            Как Notimy поможет вашему бизнесу?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-6 bg-white shadow-md rounded-lg">
              <h3 className="text-lg font-semibold text-blue-600 mb-4">
                Удобная подписка
              </h3>
              <p className="text-gray-700">
                Просто запустите сервис с помощью подписки и получайте доступ к созданию каналов для ваших клиентов.
              </p>
            </div>
            <div className="p-6 bg-white shadow-md rounded-lg">
              <h3 className="text-lg font-semibold text-blue-600 mb-4">
                Реальное время отслеживания
              </h3>
              <p className="text-gray-700">
                Ваши клиенты могут отслеживать заказы в реальном времени прямо через браузер, без необходимости
                скачивать приложение.
              </p>
            </div>
            <div className="p-6 bg-white shadow-md rounded-lg">
              <h3 className="text-lg font-semibold text-blue-600 mb-4">
                Интуитивно понятный интерфейс
              </h3>
              <p className="text-gray-700">
                Простота использования, как для бизнеса, так и для ваших клиентов.<br/> Подключение каналов и управление
                заказами не требует дополнительных усилий.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="bg-gray-100 p-10 drop-shadow-2xl">
        <div className="container mx-auto">
          <h2 className="text-3xl font-semibold text-center mb-8">
            Почему бизнесы выбирают Notimy?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {["Упрощение процессов обслуживания клиентов",
              "Минимизация ожидания и увеличение клиентского удовлетворения",
              "Мгновенное подключение и интеграция",
              "Экономия на разработке собственных решений",
              "Отслеживание заказов и улучшение коммуникации с клиентами",
              "Прозрачность процессов для клиентов"].map((benefit, index) => (
              <div
                key={index}
                className="p-6 bg-white shadow-md rounded-lg text-center"
              >
                <h3 className="text-lg font-semibold text-blue-600 mb-4">
                  {benefit}
                </h3>
                <p className="text-gray-700">
                  Подробности о том, как {benefit} и как это поможет улучшить ваше обслуживание клиентов и снизить
                  затраты.
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Subscription Plans Section */}
      <section id="plans" className="py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-semibold text-center mb-8">
            Подпишитесь на удобный план для вашего бизнеса
          </h2>
          <div className="grid grid-cols-2 gap-8 drop-shadow-xl">
            <div
              className="flex flex-col p-6 bg-white shadow-md rounded-lg text-center"
            >
              <h3 className="text-2xl font-semibold text-blue-600 mb-4">
                Стандарт
              </h3>
              <p className="text-2xl font-bold text-gray-700 mb-4">
                <span className="line-through text-gray-400 text-base" >₽3.000</span> <span className="text-green-600">₽1.000/месяц</span>
              </p>
              <ul className="self-center w-fit text-left text-gray-700 mb-6">
                <li className="mb-2">- 1 заведение</li>
                <li className="mb-2">- Неограниченное количество каналов</li>
                <li className="mb-2">- Система уведомлений</li>
              </ul>
              <button className="mt-auto bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                Подписаться
              </button>
            </div>
            <div className="flex flex-col p-6 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-2xl font-semibold text-blue-600 mb-4">
                Премиум
              </h3>
              <p className="text-2xl font-bold text-gray-700 mb-4">
                Договорная цена
              </p>
              <ul className="self-center w-fit text-left text-gray-700 mb-6">
                <li className="mb-2">- Экран заказов</li>
                <li className="mb-2">- Собственный дизайн</li>
              </ul>
              <button className="mt-auto bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                Подписаться
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cta" className="bg-blue-600 py-16 text-white rounded-t-2xl">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Готовы начать?</h2>
          <p className="text-lg mb-8">
            Начните работу с Notimy сегодня и улучшите клиентский опыт.
          </p>
          <Link href={siteConfig.links.telegram}>
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100">
              Присоединиться
            </button>
          </Link>
        </div>
      </section>
    </div>
  );
}

import {siteConfig} from "@/config/site";
import {Link} from "@nextui-org/link";
import Image from 'next/image';
import React from "react";
import {FaBolt, FaEye, FaMapMarkerAlt, FaMoneyBillWave, FaSmileBeam, FaUsersCog} from 'react-icons/fa';

export default function AboutPage() {
  return (
    <div className="font-sans text-black flex flex-col gap-9">

      {/* Hero Section */}
      <section id="hero" className="bg-gray-50 py-16 rounded-2xl drop-shadow-xl">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl font-bold mb-4">
            Упростите управление очередями с Notimy
          </h1>
          <p className="text-lg mb-8">
            Открывайте удобные каналы, где клиенты отслеживают заказы в реальном времени.<br/> Всё без скачивания
            приложения — просто в браузере.
          </p>
          <Link href={siteConfig.links.telegram}>
            <button className="bg-[#9595F6] text-white px-6 py-3 rounded-lg shadow-lg hover:bg-black-400">
              Присоединиться
            </button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="flex flex-wrap p-3">
        <div className="flex-1 flex flex-col justify-center min-w-[300px]">
          <div className="text-3xl font-semibold text-center mb-8">Современный интерфейс</div>
          <div className="text-3xl font-semibold text-center mb-8">Лёгкое управление</div>
          <div className="text-3xl font-semibold text-center mb-8">Максимальная прозрачность</div>
          <div className="text-3xl font-semibold text-center mb-8">Увеличение эффективности</div>
        </div>
        <div className="flex justify-center items-center min-w-[300px]">
          <Image
            src="/notimy phone.png"
            alt="Example Image"
            width={500}
            height={400}
            className="object-contain"
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
              <h3 className="text-lg font-semibold text-black mb-4">
                Удобная подписка
              </h3>
              <p className="text-black">
                Просто запустите сервис с помощью подписки и получайте доступ к созданию каналов для ваших клиентов.
              </p>
            </div>
            <div className="p-6 bg-white shadow-md rounded-lg">
              <h3 className="text-lg font-semibold text-black mb-4">
                Реальное время отслеживания
              </h3>
              <p className="text-black">
                Ваши клиенты могут отслеживать заказы в реальном времени прямо через браузер, без необходимости
                скачивать приложение.
              </p>
            </div>
            <div className="p-6 bg-white shadow-md rounded-lg">
              <h3 className="text-lg font-semibold text-black mb-4">
                Интуитивно понятный интерфейс
              </h3>
              <p className="text-black">
                Простота использования, как для бизнеса, так и для ваших клиентов.<br/> Подключение каналов и управление
                заказами не требует дополнительных усилий.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="bg-gray-50 p-5 drop-shadow-2xl">
        <div className="container mx-auto">
          <h2 className="text-3xl font-semibold text-center mb-8 ">
            Почему бизнесы выбирают Notimy?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Benefit 1 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-start">
                <FaUsersCog className="text-7xl text-[#9595F6]"/> {/* Margin-right for spacing */}
                Упрощение процессов обслуживания клиентов
              </h3>
              <p className="text-black">
                Обеспечьте удобное взаимодействие с клиентами, оптимизируя их опыт и ускоряя процессы.
              </p>
            </div>
            {/* Benefit 2 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-center">
                <FaSmileBeam className="text-7xl text-[#9595F6]"/>
                Минимизация ожидания и увеличение клиентского удовлетворения
              </h3>
              <p className="text-black">
                Сократите время ожидания клиентов и увеличьте их лояльность с помощью инновационных решений.
              </p>
            </div>
            {/* Benefit 3 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-start">
                <FaBolt className="text-5xl mr-3 text-[#9595F6]"/> {/* Margin-right for spacing */}
                Мгновенное подключение и интеграция
              </h3>
              <p className="text-black">
                Легкое подключение к вашим существующим системам без необходимости долгих внедрений.
              </p>
            </div>
            {/* Benefit 4 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-start">
                <FaMoneyBillWave className="text-7xl text-[#9595F6]"/> {/* Margin-right for spacing */}
                Экономия на разработке собственных решений
              </h3>
              <p className="text-black">
                Сэкономьте бюджет на разработке уникальных инструментов, воспользовавшись готовым сервисом.
              </p>
            </div>
            {/* Benefit 5 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-start">
                <FaMapMarkerAlt className="text-7xl text-[#9595F6]"/> {/* Margin-right for spacing */}
                Отслеживание заказов и улучшение коммуникации с клиентами
              </h3>
              <p className="text-black">
                Отслеживайте статус заказов и предоставляйте актуальную информацию своим клиентам.
              </p>
            </div>
            {/* Benefit 6 */}
            <div className="p-4 bg-white shadow-md rounded-lg text-center">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center justify-start">
                <FaEye className="text-7xl text-[#9595F6]"/> {/* Margin-right for spacing */}
                Прозрачность процессов для клиентов
              </h3>
              <p className="text-black">
                Обеспечьте прозрачность на всех этапах обслуживания, завоевывая доверие ваших клиентов.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Subscription Plans Section */}
      <section id="plans" className="py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-semibold text-center mb-8">
            Подпишитесь на удобный план для вашего бизнеса
          </h2>
          <div className="flex flex-wrap justify-center gap-8 drop-shadow-xl">
            {/* Standard Plan */}
            <div className="flex flex-col p-6 bg-white shadow-md rounded-lg text-center flex-1 max-w-sm min-h-[300px]">
              <h3 className="text-2xl font-semibold text-black mb-4">
                Стандарт
              </h3>
              <p className="text-2xl font-bold text-black mb-4">
                <span className="line-through text-black text-base">₽3.000</span> <span
                className="text-green-600">₽1.000/месяц</span>
              </p>
              <ul className="self-center w-fit text-left text-black mb-6">
                <li className="mb-2">- 1 заведение</li>
                <li className="mb-2">- Неограниченное количество каналов</li>
                <li className="mb-2">- Система уведомлений</li>
              </ul>
              <button className="mt-auto bg-[#9595F6] text-white px-6 py-3 rounded-lg hover:bg-[#9595F6]">
                Подписаться
              </button>
            </div>
            {/* Premium Plan */}
            <div className="flex flex-col p-6 bg-white shadow-md rounded-lg text-center flex-1 max-w-sm min-h-[300px]">
              <h3 className="text-2xl font-semibold text-black mb-4">
                Премиум
              </h3>
              <p className="text-2xl font-bold text-black mb-4">
                Договорная цена
              </p>
              <ul className="self-center w-fit text-left text-black mb-6">
                <li className="mb-2">- Экран заказов</li>
                <li className="mb-2">- Собственный дизайн</li>
              </ul>
              <button className="mt-auto bg-[#9595F6] text-white px-6 py-3 rounded-lg hover:bg-[#9595F6]">
                Подписаться
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cta" className="bg-gray-50 py-16 text-black rounded-t-2xl">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Готовы начать?</h2>
          <p className="text-lg mb-8">
            Начните работу с Notimy сегодня и улучшите клиентский опыт.
          </p>
          <Link href={siteConfig.links.telegram}>
            <button className="bg-[#9595F6] text-white px-6 py-3 rounded-lg shadow-lg hover:bg-[#9595F6]">
              Присоединиться
            </button>
          </Link>
        </div>
      </section>
    </div>
  );
}

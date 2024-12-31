import {
  Navbar as NextUINavbar,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
  NavbarBrand,
  NavbarMenuItem,
} from "@nextui-org/navbar";
import { Link } from "@nextui-org/link";
import NextLink from "next/link";
import { siteConfig } from "@/config/site";
import { TelegramIcon, Logo } from "@/components/icons";

export const Navbar = () => {
  return (
    <NextUINavbar className="w-full flex fixed top-0 z-50">
      {/* Left side: Brand */}
      <NavbarContent className="basis-1/5 sm:basis-auto" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex" href="/">
            <Logo />
            <p className="font-bold text-4xl">OTIMY</p>
          </NextLink>
        </NavbarBrand>
      </NavbarContent>

      {/* Right side: Menu */}
      <NavbarContent
        className="hidden sm:flex basis-4/5 sm:basis-auto"
        justify="end"
      >
        <Link href="#hero" className="text-gray-600 hover:text-gray-800">
          Главная
        </Link>
        <Link href="#features" className="text-gray-600 hover:text-gray-800">
          Особенности
        </Link>
        <Link href="#benefits" className="text-gray-600 hover:text-gray-800">
          Преимущества
        </Link>
        <Link href="#plans" className="text-gray-600 hover:text-gray-800">
          Планы
        </Link>
        <Link href="#cta" className="text-gray-600 hover:text-gray-800">
          Контакты
        </Link>
        <Link
          isExternal
          aria-label="Telegram"
          href={siteConfig.links.telegram}
          className="flex items-center border-2 rounded-xl p-2 hover:bg-gray-100"
        >
          <span className="text-gray-900 hover:text-gray-700 whitespace-nowrap">
            Связаться с нами
          </span>
          <TelegramIcon className="ml-2 text-default-500" />
        </Link>
      </NavbarContent>

      {/* Menu Toggle (visible on small screens) */}
      <NavbarMenuToggle className="sm:hidden" />

      {/* Mobile Menu */}
      <NavbarMenu className="sm:hidden">
        <NavbarMenuItem>
          <Link href="#hero">Главная</Link>
        </NavbarMenuItem>
        <NavbarMenuItem>
          <Link href="#features">Особенности</Link>
        </NavbarMenuItem>
        <NavbarMenuItem>
          <Link href="#benefits">Преимущества</Link>
        </NavbarMenuItem>
        <NavbarMenuItem>
          <Link href="#plans">Планы</Link>
        </NavbarMenuItem>
        <NavbarMenuItem>
          <Link href="#cta">Контакты</Link>
        </NavbarMenuItem>
        <NavbarMenuItem>
          <Link isExternal href={siteConfig.links.telegram}>
            Связаться с нами
          </Link>
        </NavbarMenuItem>
      </NavbarMenu>
    </NextUINavbar>
  );
};

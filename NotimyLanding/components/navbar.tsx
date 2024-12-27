import {
  Navbar as NextUINavbar,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
  NavbarBrand,
  NavbarItem,
  NavbarMenuItem,
} from "@nextui-org/navbar";
import { Button } from "@nextui-org/button";
import { Kbd } from "@nextui-org/kbd";
import { Link } from "@nextui-org/link";
import { Input } from "@nextui-org/input";
import { link as linkStyles } from "@nextui-org/theme";
import NextLink from "next/link";
import clsx from "clsx";

import { siteConfig } from "@/config/site";
import { ThemeSwitch } from "@/components/theme-switch";
import {
  TwitterIcon,
  GithubIcon,
  DiscordIcon,
  HeartFilledIcon,
  SearchIcon,
  Logo, TelegramIcon,
} from "@/components/icons";
import {useTheme} from "next-themes";

export const Navbar = () => {

  return (
    <NextUINavbar maxWidth="xl" position="sticky">
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex" href="/">
            <Logo />
            <p className="font-bold text-4xl">OTIMY</p>
          </NextLink>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent
        className="sm:flex basis-1/5 sm:basis-full"
        justify="end"
      >

        <Link isExternal aria-label="Telegram" href={siteConfig.links.telegram}>
        <NavbarItem className="sm:flex border-2 rounded-xl p-2">
            <span className="text-gray-900 hover:text-gray-700">Связаться с нами</span>
            <TelegramIcon className="text-default-500" />
        </NavbarItem>
        </Link>
          {/*<NavbarItem className="sm:flex gap-3">*/}
        {/*  <ThemeSwitch />*/}
        {/*</NavbarItem>*/}
      </NavbarContent>
    </NextUINavbar>
  );
};

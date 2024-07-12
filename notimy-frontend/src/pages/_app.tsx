import React from "react";
import { AppProps } from 'next/app';
import Head from 'next/head';

import Header from "../components/layout/Header/Header";


import 'normalize.css'
import '../assets/styles/global.css';
import styles from '../assets/styles/global.module.css';


function MyApp({ Component, pageProps }: AppProps) {
  return (
      <>
          <Head>
              <title>Notimy</title>
              <meta name="description" content="Notimy - в пизду пейджеры"/>
              <meta name="viewport" content="width=device-width, initial-scale=1"/>
              <link rel="icon" href="/logo.svg"/>
              <link rel="preconnect" href="https://fonts.googleapis.com"/>
              <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin/>
              <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap"
                    rel="stylesheet"/>
          </Head>

          <Component {...pageProps} />;
      </>
  );
}

export default MyApp;

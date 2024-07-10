import '../assets/styles/global.module.css';
import 'normalize.css'
import { AppProps } from 'next/app';
import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Notimy</title>
        <meta name="description" content="Notimy - в пизду пейджеры" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/logo.svg" />
      </Head>
      <Component {...pageProps} />;
    </>
  );
}

export default MyApp;

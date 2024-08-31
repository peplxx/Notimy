import React from 'react';

import styles from './Header.module.css';


const Header = ({children}) => {
  return (
      <div className={styles.header}>
          <img src='/logo.svg' alt='logo' className={styles.logo}></img>
          <div className={styles.text}>
            OTIMY
          </div>
          {children}
      </div>
  )
};

export default Header

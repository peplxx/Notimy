import React from 'react';

import styles from './Header.module.css'


const Header: React.FC = () => {
  return (
      <div className={styles.header}>
          <img src='/logo.svg' className={styles.logo}></img>
          <div className={styles.text}>
            OTIMY
          </div>
      </div>
  );
};

export default Header;

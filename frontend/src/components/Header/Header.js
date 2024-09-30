import React from 'react';

import styles from './Header.module.css';


const Header = ({withLogo=true, children}) => {
  return (
      <div className={styles.header}>
          {withLogo?
              <>
              <img src='/logo.svg' alt='logo' className={styles.logo}></img>
              <div className={styles.text}>
                OTIMY
              </div>
              </>
              :
              <img src='/logo.svg' alt='logo' className={styles.logo} style={{position: "absolute", left: "1em"}} />
          }
          {children}
      </div>
  )
};

export default Header

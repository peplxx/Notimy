import React from 'react';

import styles from './Header.module.css'

interface Props {
  title: string;
}

const Header: React.FC<Props> = ({ title }) => {
  return <header className={styles.container}>
      <div className={styles.letter}>
          <span className={styles.irregularShape}>N</span>
          <span className={styles.irregularShape}>O</span>
          <span className={styles.irregularShape}>T</span>
          <span className={styles.irregularShape}>I</span>
          <span className={styles.irregularShape}>M</span>
          <span className={styles.irregularShape}>Y</span>
      </div>
  </header>;
};

export default Header;

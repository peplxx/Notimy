import Header from '@/components/layout/Header/Header';
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css';
import { OrdersProvider} from '@/components/hooks/OrdersContext';

const App: React.FC = () => {
    return (
        <div className={styles.App}>
            <Header/>
            <OrderList />
        </div>
    );
};

const Root: React.FC = () => (
    <OrdersProvider>
        <App />
    </OrdersProvider>
);

export default Root;

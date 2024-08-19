import axiosInstance from '@/utils/axiosInstance';
import { GetServerSideProps } from 'next';

const Spot: React.FC = () => {
    return <></>; // Nothing to render as we're handling redirection in `getServerSideProps`
};

export const getServerSideProps: GetServerSideProps = async (context) => {
    const { id } = context.params!;

    const response = await axiosInstance.get(`/spot/${id}`, {withCredentials: true});

    return {
        redirect: {
            destination: '/',
            permanent: false,
        },
    };
};

export default Spot;

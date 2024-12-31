import { mock, mockList } from './mockData';

let counter = 1;

export const handleMockOrders = () => {
    if (counter % 2 === 0 && counter % 4 !== 0) {
        const newMock = { ...mock, id: counter.toString() };
        mockList.push(newMock);
    } else if (counter % 4 === 0 && mockList.length > 0) {
        mockList[mockList.length - 1].open = false;
    }
    counter += 1;
    return [...mockList];
};

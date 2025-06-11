// Counter.js
import React, { useState } from 'react';

// Компонент "спостерігач" за одним лічильником
const CounterDisplay = ({ count, name }) => {
    console.log(`${name} відрендерився`);
    return <p>{name}: {count}</p>;
};

// Головний компонент із суб’єктом (станом)
const CounterApp = () => {
    const [counterA, setCounterA] = useState(0);
    const [counterB, setCounterB] = useState(0);

    const incrementA = () => setCounterA(counterA + 1);
    const incrementB = () => setCounterB(counterB + 1);

    return (
        <div>
            <h1>Динамічні лічильники</h1>
            <CounterDisplay count={counterA} name="Лічильник A" />
            <CounterDisplay count={counterB} name="Лічильник B" />
            <button onClick={incrementA}>Збільшити A</button>
            <button onClick={incrementB}>Збільшити B</button>
        </div>
    );
};

export default CounterApp;

// App.js
import React from 'react';
import CounterApp from './Counter';

const App = () => {
    return (
        <div>
            <CounterApp />
        </div>
    );
};

export default App;

// index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));
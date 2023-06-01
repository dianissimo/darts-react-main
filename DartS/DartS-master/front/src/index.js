// React фронтальная часть приложения работает только с darts-mysql-flask-small задней частью приложения
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './app';

// Определение устройства приложения
ReactDOM.render(
    <Router>
        <App />
    </Router>,
    document.getElementById('root')
);

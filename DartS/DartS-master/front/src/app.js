// React фронтальная часть приложения работает только с darts-mysql-flask-small задней частью приложения
import React from 'react';
import LongreadEdit from './components/main';
import LongreadsList from './components/main';
import Longread from './components/main';
import LongreadCreate from './components/main';
// React-Router-Dom используется для создания путей в приложении
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

// Определение путей, которые используются в React фронтальном приложении
function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component={LongreadsList} />
                <Route exact path="/longreads/:longreadId" component={Longread} />
                <Route exact path="/longreads/:longreadId/edit" component={LongreadEdit} />
                <Route exact path="/create" component={LongreadCreate} />
            </Switch>
        </Router>
    );
}

export default App;

// React фронтальная часть приложения работает только с darts-mysql-flask-small задней частью приложения
// useEffect используется для того чтобы запросить данные у задней части приложения
// useState используется длся того чтобы иметь переменные которые можно обновлять по ходу работы приложения
import React, { useEffect, useState } from 'react';
// useHistory используется для редиректа на другой путь
import { BrowserRouter as Router, Switch, Route, Link, useHistory } from 'react-router-dom';
// axios клиент используется для отсылки запросов
import axios from 'axios';


// Функция для отображения списка лонгридов
function LongreadsList() {
    // useState переменные
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [longreads, setLongreads] = useState([]);

    // GET запрос на сервер для получения списка лонгридов
    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/explore/')
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                // Отображение загрузки прекратится
                setLoading(false);
                // Список лонгридов будет записан в переменную longreads
                setLongreads(response.data);
            })
            // Обработка ошибки
            .catch(error => {
                setLoading(false);
                console.error('Error fetching longreads:', error);
                setError('Error fetching longreads' + error.message);
            });
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }
    // Отображение фронтальной части приложения
    return (
        <div>
            <Link to="/create">Create Longread</Link>
            <h2>Longreads List</h2>
            {/*С помощью map вложенных в ответ список лонгридов можно отобразить по одному*/}
            {longreads.map(longread => (
                <div key={longread.id}>
                    <h3>
                        <Link to={`/longreads/${longread.id}`}>{longread.name}</Link>
                    </h3>
                </div>
            ))}
        </div>
    );
}

// Функция для отображения лонгрида
function Longread({ match }) {
    // useState переменные
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [longread, setLongread] = useState(null);
    // useHistory переменная для возвращения на индексную страницу
    const history = useHistory();
    const [newImage, setNewImage] = useState(null);

    // Функция для изменения переменной файла при его добавлении
    const handleImageChange = (e) => {
        setNewImage(e.target.files[0]);
    };

    // Функция для изменения изображения лонгрида
    const handleImageUpload = () => {
        // Создание нового объекта FormData
        const formData = new FormData();

        // Добавление нового файла в объект formData
        formData.append('image', newImage);

        // Отправка файла POST запросом на заднюю часть приложения
        axios.post(`http://127.0.0.1:5000/api/longreads/${match.params.longreadId}/update-image`, formData)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                console.log('Image updated:', response.data);
                history.push(`/`);
            })
            // Обработка ошибки
            .catch(error => {
                console.error('Error updating image:', error);
                // Handle the error accordingly
            });
    };

    // GET запрос на сервер для получения данных лонгрида
    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/api/longreads/${match.params.longreadId}`)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                // Отображение загрузки прекратится
                setLoading(false);
                // Данные лонгрида будут записан в переменную longread
                setLongread(response.data);
            })
            // Обработка ошибки
            .catch(error => {
                setLoading(false);
                console.error('Error fetching longread:', error);
                setError('Error fetching longread' + error.message);
            });
    }, [match.params.longreadId]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    if (!longread) {
        return null;
    }

    // Функция для удаления лонгрида
    const handleDelete = () => {
        axios
            .delete(`http://127.0.0.1:5000/api/longreads/${longread.id}/delete`)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                console.log('Longread deleted:', response.data);
                history.push("/");
            })
            // Обработка ошибки
            .catch(error => {
                console.error('Error deleting longread:', error);
            });
    };
    // Отображение фронтальной части приложения
    return (
        <div>
            <h2>{longread.name}</h2>
            <p>{longread.description}</p>
            <img src={longread.img_link} alt={longread.name} width="500" height="600" />
            <p>{longread.text}</p>
            {/*Окно ввода файла*/}
            <input type="file" accept="image/*" onChange={handleImageChange} />
            <button onClick={handleImageUpload}>Change Image</button>
            {/*Кнопка изменения лонгрида*/}
            <Link to={`/longreads/${longread.id}/edit`}>Edit Longread</Link>
            <button onClick={handleDelete}>Delete</button>
        </div>
    );
}


// Функция для создания лонгрида
function LongreadCreate() {
    // useState переменные
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        text: ''
    });
    const [loading, setLoading] = useState(true);
    // useHistory переменная для возвращения на индексную страницу
    const history = useHistory();

    // Функция для отправки заполненной формы
    const handleFormSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        // Отправка файла POST запросом на заднюю часть приложения
        axios.post('http://127.0.0.1:5000/api/longreads/create', formData)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                setLoading(false);
                console.log('Longread created:', response.data);
                history.push("/");
            })
            // Обработка ошибки
            .catch(error => {
                setLoading(false);
                console.error('Error creating longread:', error);
            });
    };

    // Функция для осуществления работоспособности ввода формы
    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    // Отображение фронтальной части приложения
    return (
        <div>
            <h2>Create Longread</h2>
            <form onSubmit={handleFormSubmit} method="POST">
                <div>
                    <label htmlFor="name">Name:</label>
                    <input type="text" id="name" name="name" value={formData.name} onChange={handleInputChange} />
                </div>
                <div>
                    <label htmlFor="description">Description:</label>
                    <input type="text" id="description" name="description" value={formData.description} onChange={handleInputChange} />
                </div>
                <div>
                    <label htmlFor="text">Text:</label>
                    <textarea id="text" name="text" value={formData.text} onChange={handleInputChange} />
                </div>
                <button type="submit">Create</button>
            </form>
        </div>
    );
}


// Функция для изменения лонгрида
function LongreadEdit({ match }) {
    // useState переменные
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [longread, setLongread] = useState(null);
    // useHistory переменная для возвращения на индексную страницу
    const history = useHistory();

    // GET запрос на сервер для получения данных лонгрида
    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/api/longreads/${match.params.longreadId}`)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                setLoading(false);
                setLongread(response.data);
            })
            // Обработка ошибки
            .catch(error => {
                setLoading(false);
                console.error('Error fetching longread:', error);
                setError('Error fetching longread' + error.message);
            });
    }, [match.params.longreadId]);

    // Функция для отправки заполненной формы
    const handleFormSubmit = (e) => {
        e.preventDefault();
        // Создание нового объекта FormData
        const formData = new FormData(e.target);
        // Создание заполнение объекта formData обновленными данными
        const updatedLongread = {
            name: formData.get('name'),
            description: formData.get('description'),
            text: formData.get('text'),
        };
        // Отправка файла POST запросом на заднюю часть приложения
        axios.post(`http://127.0.0.1:5000/api/longreads/${longread.id}/edit`, updatedLongread)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                console.log('Longread updated:', response.data);
                history.push("/");
            })
            // Обработка ошибки
            .catch(error => {
                console.error('Error updating longread:', error);
            });
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    if (!longread) {
        return null;
    }
    // Отображение фронтальной части приложения
    return (
        <div>
            <h2>Edit Longread</h2>
            <form onSubmit={handleFormSubmit}>
                <div>
                    <label htmlFor="name">Name:</label>
                    <input type="text" id="name" name="name" defaultValue={longread.name} />
                </div>
                <div>
                    <label htmlFor="description">Description:</label>
                    <input type="text" id="description" name="description" defaultValue={longread.description} />
                </div>
                <div>
                    <label htmlFor="text">Text:</label>
                    <textarea id="text" name="text" defaultValue={longread.text} />
                </div>
                <button type="submit">Update</button>
            </form>
        </div>
    );
}

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
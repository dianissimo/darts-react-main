import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import Card from "react-bootstrap/esm/Card";
import styled from "styled-components";
import { Breadcrumb } from "react-bootstrap";
import WorldObjects from "../components/WorldObjects";
import ListGroup from "react-bootstrap/ListGroup";
import { useLocation } from "react-router-dom";
import ChapterCard from "../components/ChapterCard";
import axios from 'axios';


export default function LongreadPage() {
    const location = useLocation();
    const longreadData = location.state.longreadData    
    // download chapters Id and names 
    // transfer longreadData along +

    // useState переменные
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [chaptersHolder, setChapters] = useState([]);

    // GET запрос на сервер для получения списка лонгридов
    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/api/longreads/${longreadData.longreadId}`)
            // Действия которые будут выполнены при успешном выполнении запроса
            .then(response => {
                // Отображение загрузки прекратится
                setLoading(false);
                // Список лонгридов будет записан в переменную longreads
                setChapters(response.data);
            })
            // Обработка ошибки
            .catch(error => {
                setLoading(false);
                console.error('Error fetching longreads:', error);
                setError('Error fetching longreads' + error.message);
            });
    }, []);

    console.log(chaptersHolder)


    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    // const chapters = ["123"]
    return (
        <div id="longread">
            <Container>
                <Breadcrumb
                    style={{
                        marginTop: "20px",
                    }}
                >
                    <StyledBreadcrumb href="/explore/longreads">Longreads</StyledBreadcrumb>
                    <StyledBreadcrumb active>{longreadData.title}</StyledBreadcrumb>
                </Breadcrumb>
                <Row xs={6} sm={2} md={2} lg={3} xl={4} className="g-4">
                    <Col xs={12} sm={12} md={12} lg={12} xl={12}>
                        <Card
                            className="bg-dark text-white"
                            style={{
                                border: "none",
                                height: "300px",
                            }}
                        >
                            <StyledImage src={longreadData.img} />
                            <Card.ImgOverlay
                                style={{
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "space-between",
                                }}
                            >
                                <Card.Title
                                    style={{
                                        fontSize: "2.5rem",
                                        color: "white",
                                    }}
                                >
                                    {longreadData.title}
                                </Card.Title>
                                <Card.Text>
                                    {longreadData.desc}
                                </Card.Text>
                            </Card.ImgOverlay>
                        </Card>
                    </Col>
                    <div
                        style={{
                            width: "100%",
                            display: "flex",
                            flexDirection: "row",
                            justifyContent: "space-between",
                            flexWrap: "wrap",
                        }}
                    >

                        <div
                            style={{
                                marginRight: "20px",
                                marginBottom: "20px",
                                flexBasis: "100%",
                                flexGrow: 1,
                            }}
                        >
                            <h3>Chapters</h3>
                            <ListGroup>
                                {chaptersHolder.chapters.map((chapter, idx) => (
                                    <ListGroup.Item key = {idx}>
                                        <ChapterCard 
                                            longreadData={longreadData}
                                            chapterData={chapter}
                                            chapterIdx={idx}
                                        />
                                    </ListGroup.Item>
                                ))}
                            </ListGroup>

                            
                        </div>
                    </div>
                </Row>
            </Container>
        </div>
    );
}

const StyledImage = styled(Card.Img)`
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 4px;
`;

const StyledBreadcrumb = styled(Breadcrumb.Item)`
  &:not(:first-child):before {
    content: "/" !important;
    color: rgba(0, 81, 85, 0.5) !important;
  }

  color: rgba(0, 81, 85, 0.5) !important;

  a {
    text-decoration: none;
    color: rgba(0, 81, 85, 1);
  }
`;

const StyledBreadcrumbActive = styled(Breadcrumb.Item)`
  // change the color
  color: rgba(0, 81, 85, 1) !important;
`;

import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row } from "react-bootstrap";
import styled from "styled-components";
import LongreadCard from "../components/LongreadCard";
import axios from 'axios';


export default function Longreads() {
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
        }); }
    , []
  );

  console.log(longreads)

  if (loading) {
      return <p>Loading...</p>;
  }

  if (error) {
      return <p>{error}</p>;
  }

  return (
    <div id="longreads">
      <Container>
        <Row xs={1} sm={1} md={1} lg={1} xl={2} className="g-4">
          <Col xl={12}>
            <Card
              className="bg-dark text-white"
              style={{
                border: "none",
                height: "300px",
              }}
            >
              <StyledImage src="../assets/dune.jpg" />
              <Card.ImgOverlay>
                <Card.Title>DUNE</Card.Title>
                <Card.Text>___________________</Card.Text>
                <Card.Text>Editor's pick</Card.Text>
              </Card.ImgOverlay>
            </Card>
          </Col>
          {longreads.map((longread, idx) => (
            <Col key={idx}>
              <LongreadCard longreadId={longread.id}
                title={longread.name}
                desc={longread.description}
                img={longread.img_link}
              />
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
}

const StyledImage = styled(Card.Img)`
  height: 100%;
  width: 100%;
  object-fit: cover;
`;

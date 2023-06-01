import React, { useEffect, useState } from 'react';
import { Card, Col, Container, Row } from "react-bootstrap";
import styled from "styled-components";
import LongreadCard from "../components/LongreadCard";

// import { BrowserRouter as Router, Switch, Route, Link, useHistory } from 'react-router-dom';
import axios from 'axios';

export default function Longreads() {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [longreads, setLongreads] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/explore/')
        .then(response => {
          setLoading(false);
          setLongreads(response.data);
        })
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
            {longreads.map(longread => (
                <Col>
                    <LongreadCard
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

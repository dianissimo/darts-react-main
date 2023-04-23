import React from "react";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import Card from "react-bootstrap/esm/Card";
import styled from "styled-components";
import { Breadcrumb } from "react-bootstrap";
import WorldObjects from "../components/WorldObjects";
import ListGroup from "react-bootstrap/ListGroup";

export default function LongreadPage() {
    return (
        <div id="longread">
            <Container>
                <Breadcrumb
                    style={{
                        marginTop: "20px",
                    }}
                >
                    <StyledBreadcrumb href="/explore/longreads">Longreads</StyledBreadcrumb>
                    <StyledBreadcrumb active>Fantastic Beasts and Where to Find Them</StyledBreadcrumb>
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
                            <StyledImage src="../assets/beasts.jpg" />
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
                                    Fantastic Beasts and Where to Find Them
                                </Card.Title>
                                <Card.Text>
                                    Fantastic Beasts and Where to Find Them is a book written by J. K. Rowling about the magical creatures in the Harry Potter universe
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
                            <h3>Longread</h3>
                            <ListGroup>
                                <ListGroup.Item>
                                    <p>Fantastic Beasts and Where to Find Them (often referred to as simply Fantastic Beasts) is a 2001 guide book written by British author J. K. Rowling (under the pen name of the fictitious author Newt Scamander) about the magical creatures in the Harry Potter universe. The original version, illustrated by the author herself, purports to be Harry Potter's copy of the textbook of the same name mentioned in Harry Potter and the Philosopher's Stone (or Harry Potter and the Sorcerer's Stone in the US), the first novel of the Harry Potter series. It includes several notes inside it supposedly handwritten by Harry, Ron Weasley, and Hermione Granger, detailing their own experiences with some of the beasts described, and including inside jokes relating to the original series.</p>
                                    <p>In a 2001 interview with publisher Scholastic, Rowling stated that she chose the subject of magical creatures because it was a fun topic for which she had already developed much information in earlier books. Rowling's name did not appear on the cover of the first edition, the work being credited under the pen name "Newt Scamander", who, in the books, wrote this textbook as seen on Harry's supply list for his first year.</p>
                                    <p>The book benefits the BBC affiliated charity Comic Relief. Over 80% of the cover price of each book sold goes directly to poor children in various places around the world. According to Comic Relief, sales from this book and its companion Quidditch Through the Ages had raised over £17 million by July 2009.</p>
                                    <p>The book benefits the BBC affiliated charity Comic Relief. Over 80% of the cover price of each book sold goes directly to poor children in various places around the world. According to Comic Relief, sales from this book and its companion Quidditch Through the Ages had raised over £17 million by July 2009. The book benefits the BBC affiliated charity Comic Relief. Over 80% of the cover price of each book sold goes directly to poor children in various places around the world. According to Comic Relief, sales from this book and its companion Quidditch Through the Ages had raised over £17 million by July 2009. The film was released on 18 November 2016.</p>
                                    <p>On 14 March 2017 a new edition of the book, with cover illustrations by Jonny Duddle and interior illustrations by Tomislav Tomic, was published with six new creatures and a foreword by Newt Scamander. It is assumed to be a new copy as it does not feature any handwritten notes. Proceeds from this edition are donated to Lumos as well as Comic Relief.</p>
                                    <p>On 7 November 2017 a new edition was published with illustrations by Olivia Lomenech Gill, featuring the aforementioned 2017 text. On 1 February 2018 a Kindle in Motion edition, featuring these illustrations with movement, was released for compatible devices.</p>
                                </ListGroup.Item>
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

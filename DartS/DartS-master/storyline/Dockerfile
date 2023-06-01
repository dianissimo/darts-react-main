FROM gradle:7.5.1 AS build
COPY --chown=gradle:gradle .. /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle build

FROM eclipse-temurin:17.0.5_8-jre-ubi9-minimal
EXPOSE 8080
COPY --from=build /home/gradle/src/build/libs/storyline-0.0.1-SNAPSHOT.jar /app/
RUN bash -c 'touch /app/storyline-0.0.1-SNAPSHOT.jar'
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom","-jar","/app/storyline-0.0.1-SNAPSHOT.jar"]
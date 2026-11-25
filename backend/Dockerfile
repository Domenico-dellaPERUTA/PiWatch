# --- STAGE 1: BUILD (JDK 27 + Maven) ---
FROM maven:3.10.0-eclipse-temurin-27 AS build
WORKDIR /app

# Cache delle dipendenze (velocizza le build successive)
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .
RUN ./mvnw dependency:go-offline

# Compilazione del codice
COPY src ./src
RUN ./mvnw clean package -DskipTests

# --- STAGE 2: RUNTIME (JRE 27 patchato per java4shell) ---
# Pinnato alla versione specifica 27.0.1.0 per garantire la sicurezza
FROM eclipse-temurin:27.0.1.0-jre-alpine-3.24
WORKDIR /app

# Best practice di sicurezza: crea un utente non-root
RUN addgroup -S piwatch && adduser -S piwatch -G piwatch

# Copia solo il JAR compilato dallo stage precedente, assegnandolo all'utente non-root
COPY --from=build --chown=piwatch:piwatch /app/target/*.jar app.jar

USER piwatch
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
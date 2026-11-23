// backend/src/main/java/it/quasar_x7/backend/BackendApplication.java
package it.quasar_x7.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
/* 
import org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration;
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration;

// Disabilita l'autoconfigurazione del DataSource e di Hibernate
@SpringBootApplication(exclude = { 
    DataSourceAutoConfiguration.class,
    HibernateJpaAutoConfiguration.class
})
*/
@SpringBootApplication
public class BackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(BackendApplication.class, args);
	}

}

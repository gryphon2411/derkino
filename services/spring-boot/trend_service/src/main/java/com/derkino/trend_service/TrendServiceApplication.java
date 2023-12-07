package com.derkino.trend_service;

import com.derkino.trend_service.documents.Title;
import com.derkino.trend_service.documents.Trend;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.kstream.TimeWindows;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.kafka.annotation.EnableKafkaStreams;
import org.springframework.kafka.support.serializer.JsonSerde;

import java.time.Duration;

@EnableKafkaStreams
@SpringBootApplication
public class TrendServiceApplication {
	private static final Logger logger = LoggerFactory.getLogger(TrendServiceApplication.class);

	@Bean
	public KStream<String, Title> kStream(StreamsBuilder builder) {
		KStream<String, Title> stream = builder.stream("title-searches", Consumed.with(Serdes.String(), new JsonSerde<>(Title.class)));

		// Group by title and window for 3 minutes
		stream.groupByKey()
				.windowedBy(TimeWindows.of(Duration.ofMinutes(3)))
				.count()
				.toStream()
				.foreach((key, value) -> logger.info("Most consumed title in the last 3 minutes (key): " + key.key() + " with count (value): " + value));

		return stream;
	}


	public static void main(String[] args) {
		SpringApplication.run(TrendServiceApplication.class, args);
	}

}
//	@Bean
//	public KStream<String, Title> kStream(StreamsBuilder streamsBuilder) {
//		KStream<String, Title> stream = streamsBuilder.stream("title-searches", Consumed.with(Serdes.String(), new JsonSerde<>(Title.class)));
//
//		// Write the trending titles by a window duration of 60 minutes to MongoDB
//		stream.map((key, value) -> new KeyValue<>(value.titleConst, value))
//				.groupByKey()
//				.windowedBy(TimeWindows.of(Duration.ofMinutes(60)))
//				.count()
//				.toStream()
//				.foreach((key, value) -> mongoTemplate.save(new Trend("title", key.key(), value), "trends"));
//
//		// Write the trending genres by a window duration of 60 minutes to MongoDB
//		stream.flatMapValues(value -> value.genres)
//				.groupBy((key, value) -> value, Grouped.with(Serdes.String(), Serdes.String()))
//				.windowedBy(TimeWindows.of(Duration.ofMinutes(60)))
//				.count()
//				.toStream()
//				.foreach((key, value) -> mongoTemplate.save(new Trend("genre", key.key(), value), "trends"));
//
//		return stream;
//	}
//}

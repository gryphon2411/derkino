package com.derkino.trend_service.documents;

import org.springframework.data.annotation.Id;

public class Trend {
    @Id
    public String id;
    public String type;
    public String value;
    public long count;

    public Trend(String type, String value, long count) {
        this.type = type;
        this.value = value;
        this.count = count;
    }
}

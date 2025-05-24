参考文档：https://postgis.net/docs/manual-dev/zh_Hans/using_postgis_dbmanagement.html#PostGIS_Geography

## pom 依赖

maven 工程引入依赖：

```xml
<dependency>
    <groupId>net.postgis</groupId>
    <artifactId>postgis-jdbc</artifactId>
    <version>2.5.1</version>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.3.6</version>
</dependency>
```

## 库表准备

创建包含存储 WGS84 大地坐标系 (SRID 4326)的地理类型列：

```sql
CREATE TABLE global_points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    location geography(POINT,4326)
);
```

对地理类型字段增加索引：
```sql
CREATE INDEX global_points_gix ON global_points USING GIST ( location );
```

插入数据：

```sql
INSERT INTO global_points (name, location) VALUES ('Town', 'SRID=4326;POINT(-110 30)');
INSERT INTO global_points (name, location) VALUES ('Forest', 'SRID=4326;POINT(-109 29)');
INSERT INTO global_points (name, location) VALUES ('London', 'SRID=4326;POINT(0 49)');
```

## 创建 TypeHandler 实现类

```java
import org.apache.commons.lang3.StringUtils;
import org.apache.ibatis.type.BaseTypeHandler;
import org.apache.ibatis.type.JdbcType;
import org.apache.ibatis.type.MappedJdbcTypes;
import org.apache.ibatis.type.MappedTypes;
import org.postgis.PGgeometry;

import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Objects;

@MappedTypes({Object.class})
@MappedJdbcTypes({JdbcType.OTHER})
public class PGgeometryTypeHandler extends BaseTypeHandler<PGgeometry> {

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, PGgeometry parameter, JdbcType jdbcType) throws SQLException {
        if(Objects.nonNull(parameter)) {
            PGgeometry pGgeometry = new PGgeometry(parameter.toGeometryStr());
            ps.setObject(i, pGgeometry);
        }
    }

    @Override
    public PGgeometry getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String string = rs.getString(columnName);
        return getResult(string);
    }

    @Override
    public PGgeometry getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        String string = rs.getString(columnIndex);
        return getResult(string);
    }

    @Override
    public PGgeometry getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        String string = cs.getString(columnIndex);
        return getResult(string);
    }


    private PGgeometry getResult(String string) throws SQLException {
        if(StringUtils.isBlank(string)) {
            return null;
        }
        return new PGgeometry(string);
    }

}
```

## 数据库对象字段

```java

public class {
     /**
     * 地理位置
     */
    @TableField(value = "location", typeHandler = PGgeometry.class)
    private PGgeometry location;
}

```



## 扩展

查询 postgis 可支持的空间参考坐标系：

```sql
SELECT * from spatial_ref_sys
```


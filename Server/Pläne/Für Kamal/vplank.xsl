<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html"/>

<xsl:template match="/vp">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="vplan.css" />
      <title><xsl:value-of select="kopf/titel"/></title>
    </head>
    <body>
      <xsl:apply-templates />
    </body>
  </html>
</xsl:template>

<xsl:template match="kopf">
  <p>
    <span class="vpfuer">Vertretungsplan für: <span class="vpfuerdatum"><xsl:value-of select="titel"/></span></span>
    <br/>
    <span class="vpschulname"><xsl:value-of select="schulname"/></span>
    <br/>
    <span class="vpdatum"><xsl:value-of select="datum"/></span>
  </p>
  <p>
    <xsl:apply-templates select="kopfinfo"/>
  </p>
</xsl:template>

<xsl:template match="freietage">
</xsl:template>

<xsl:template match="kopfinfo">
  <table class='tablekopf'>
    <xsl:if test="count(abwesendl)">
      <tr>
        <th class="thkopfabwesend">Abwesende Lehrer:</th>
        <td class="thabwesend"><xsl:value-of select="abwesendl"/></td>
      </tr>
    </xsl:if>
    <xsl:if test="count(abwesendk)">
      <tr>
        <th class="thkopfabwesend">Abwesende Klassen:</th>
        <td class="thabwesend"><xsl:value-of select="abwesendk"/></td>
      </tr>
    </xsl:if>
    <xsl:if test="count(abwesendr)">
      <tr>
        <th class="thkopfabwesend">Nicht verfügbare Räume:</th>
        <td class="thabwesend"><xsl:value-of select="abwesendr"/></td>
      </tr>
    </xsl:if>
    <xsl:if test="count(aenderungl)">
      <tr>
        <th class="thkopfabwesend">Lehrer mit Änderung:</th>
        <td class="thabwesend"><xsl:value-of select="aenderungl"/></td>
      </tr>
    </xsl:if>
    <xsl:if test="count(aenderungk)">
      <tr>
        <th class="thkopfabwesend">Klassen mit Änderung:</th>
        <td class="thabwesend"><xsl:value-of select="aenderungk"/></td>
      </tr>
    </xsl:if>
  </table>
</xsl:template>

<xsl:template match="aufsichten">
  <p>
    <span class="aufsichtenkopf">Geänderte Aufsichten:</span>
    <table>
      <xsl:apply-templates select="aufsichtzeile"/>
    </table>
  </p>
</xsl:template>

<xsl:template match="aufsichtzeile">
  <tr>
    <td class="aufsichtendetails"><xsl:value-of select="aufsichtinfo"/></td>
  </tr>
</xsl:template>

<xsl:template match="haupt">
  <p>
    <span class="ueberschrift">Geänderte Unterrichtsstunden:</span>
  </p>
  <p>
    <table border="2" class='tablekopf'>
      <tr>
        <th class="thplanklasse">Klasse/Kurs</th>
        <th class="thplanstunde">Stunde</th>
        <th class="thplanfach">Fach</th>
        <th class="thplanlehrer">Lehrer</th>
        <th class="thplanraum">Raum</th>
        <th class="thplaninfo">Info</th>
      </tr>
      <xsl:apply-templates select="aktion"/>
    </table>
  </p>
</xsl:template>

<xsl:template match="aktion">
  <tr>
    <td class="tdaktionen"><xsl:value-of select="klasse"/></td>
    <td class="tdaktionen"><xsl:value-of select="stunde"/></td>

    <xsl:choose>
      <xsl:when test="fach/@fageaendert='ae'">
        <td class="tdaktionenneu"><xsl:value-of select="fach"/></td>
      </xsl:when>
      <xsl:otherwise>
        <td class="tdaktionen"><xsl:value-of select="fach"/></td>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:choose>
      <xsl:when test="lehrer/@legeaendert='ae'">
        <td class="tdaktionenneu"><xsl:value-of select="lehrer"/></td>
      </xsl:when>
      <xsl:otherwise>
        <td class="tdaktionen"><xsl:value-of select="lehrer"/></td>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:choose>
      <xsl:when test="raum/@rageaendert='ae'">
        <td class="tdaktionenneu"><xsl:value-of select="raum"/></td>
      </xsl:when>
      <xsl:otherwise>
        <td class="tdaktionen"><xsl:value-of select="raum"/></td>
      </xsl:otherwise>
    </xsl:choose>

    <td class="tdaktionen"><xsl:value-of select="info"/></td>
  </tr>
</xsl:template>

<xsl:template match="klausuren">
  <p>
    <span class="ueberschrift">Klausuren:</span>
  </p>
  <p>
    <table border="2" class='tablekopf'>
      <tr>
        <th class="thplaninfo">Jahrgang</th>
        <th class="thplaninfo">Kurs</th>
        <th class="thplaninfo">Kursleiter</th>
        <th class="thplaninfo">Stunde</th>
        <th class="thplaninfo">Beginn</th>
        <th class="thplaninfo">Dauer</th>
        <th class="thplaninfo">Info</th>
      </tr>
      <xsl:apply-templates select="klausur"/>
    </table>
  </p>
</xsl:template>

<xsl:template match="klausur">
  <tr>
    <td class="tdaktionen"><xsl:value-of select="jahrgang"/></td>
    <td class="tdaktionen"><xsl:value-of select="kurs"/></td>
    <td class="tdaktionen"><xsl:value-of select="kursleiter"/></td>
    <td class="tdaktionen"><xsl:value-of select="stunde"/></td>
    <td class="tdaktionen"><xsl:value-of select="beginn"/></td>
    <td class="tdaktionen"><xsl:value-of select="dauer"/></td>
    <td class="tdaktionen"><xsl:value-of select="kinfo"/></td>
  </tr>
</xsl:template>

<xsl:template match="fuss">
  <p>
    <span class="ueberschrift">Zusätzliche Informationen:</span>
    <table>
      <xsl:apply-templates select="fusszeile"/>
    </table>
  </p>
</xsl:template>

<xsl:template match="fusszeile">
  <tr>
    <td><xsl:value-of select="fussinfo"/></td>
  </tr>
</xsl:template>

</xsl:stylesheet>
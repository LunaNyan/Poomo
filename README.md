# Poomo
푸모(Poomo)는 ECB 기반 바이너리 암호화 + 선택 가능한 gzip 압축 포맷입니다.

# 특징
- 4-Shard 코드북 암호화 체계이며, 평문 블록과 암호문 블록이 일대일 관계를 유지합니다.
- 암호문을 살펴보는 것만으로도 평문 속에 패턴의 반복이 있다는 것을 알게 되며, 이것을 실마리로 암호를 해독할 수 있게 됩니다. 따라서 Poomo는 **안전한 암호화 방식이 아닙니다.**
- Poomo2에서 AES로 암호화 타입이 바뀌었습니다. 현재 레포지토리는 더 이상 지원되지 않습니다. 

# 구조
## PUMO (Codebook)
 - 0 : PUMO (Magic)
 - 10 (Ah) : Timestamp in big endian
 - 100 (64h) : Codebook Block A
 - 300 (12Ch) : Codebook Block B
 - 700 (2BCh) : Codebook Block C
 - 1000 (3E8h) : Codebook Block D
 - 1290 (50Ah) : FUTAGOHIME (Tail)

## EPUMO (Encrypted Binary)
 - 0 : EPUMO (Magic)
 - 7 : CP (Compress Indicator)
 - 10 (Ah) : Size of File in big endian
 - 100 (64h) : **Reversed** Binary in Encrypted Format
 - END - 10 (Ah) : FUTAGOHIME (Tail)

# 사용 방법
 - newPoomo.py [Output]
 - poomoEncode.py [Poomo] [Victim] [Output] (nocomp)
 - poomoDecode.py [Poomo] [EPUMO] [Output]

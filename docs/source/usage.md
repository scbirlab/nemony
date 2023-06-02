# Usage

## Command line

You can use nemony to encode lines of text from a file 
(the header info goes to `stderr`).

```bash
$ printf 'hello\nworld' > tmp.txt
$ nemony tmp.txt

## MNEMO: Generate adjective-noun mnemonics
Word list version: fancy_telecom
 - Number of adjectives: 581
 - Number of nouns: 1450
 - Combinations: 842450

decorous_block
late_kevin
```

Or pipe from from `stdin`.

```bash
$ printf 'hello\nworld' | nemony 

## MNEMO: Generate adjective-noun mnemonics
Word list version: fancy_telecom
 - Number of adjectives: 581
 - Number of nouns: 1450
 - Combinations: 842450

decorous_block
late_kevin
```

You can also run interactively to check one thing at a time.
Bear in mind that this encodes the whole text, not one line 
a time.

```bash
$ nemony -i

## MNEMO: Generate adjective-noun mnemonics
Word list version: fancy_telecom
 - Number of adjectives: 581
 - Number of nouns: 1450
 - Combinations: 842450


(Ctrl-C to exit.)
What would you like to encode?

?> hello
decorous_block
?> world
late_kevin
?> hello\nworld
warm_dominic
```

```
usage: nemony [-h] [--interactive] [--output [OUTPUT]] [input]

Encode lines of text deterministically as adjective-noun mnemonics.

positional arguments:
  input                 File to read and emit one mnemonic per line. Default STDIN.

options:
  -h, --help            show this help message and exit
  --interactive, -i     Run interactively.
  --output [OUTPUT], -o [OUTPUT]
                        Output file. Default STDOUT.
```

## Python API

You can import **nemony** and use it to encode Python objects, as
long as they can be converted to strings.

```python
>>> import nemony as nm
>>> nm.encode('world', sep='-')
'late-kevin'
>>> nm.encode('world', sep='-', n=5)
'peppy-gabriel'
>>> nm.encode(5.)
'live_drum'
>>> nm.encode(['hello', 'world'])
'receding_cheese'
```

As a convenience, you can also use the SHA-256 hashing functions 
(which use Python standard library `hashlib`).

```python
>>> nm.hash('world')
'486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7'
>>> nm.hash('world', n=8)
'486ea462'
>>> nm.hash(5., n=8)
'a19a1584'
```
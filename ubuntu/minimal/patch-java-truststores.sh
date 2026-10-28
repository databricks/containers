#!/bin/sh
set -eu
export LC_ALL=C

blocked_file=${1:-/tmp/blocked.certs}
test -s "$blocked_file"

# SHA-256 fingerprints of AAA Certificate Services and emSign ECC Root CA - G3.
distrusted_roots='d7a7a0fb5d7e2731d771e9484ebcdef71d5f0c3e0a2948782bc83ee0ea699ef4 86a1ecba089c4a8d3bbe2734c612ba341d813e043cf9e8a862cd5c57a36bbe6b'

find_distrusted_aliases() {
  keytool=$1
  store=$2
  # Keep the listing in a variable so that a keytool failure stops the script.
  listing=$("$keytool" -list -v -keystore "$store" -storepass changeit)
  printf '%s\n' "$listing" \
    | awk -v roots="$distrusted_roots" '
        BEGIN {
          count = split(roots, fingerprints, " ")
          for (i = 1; i <= count; i++) {
            distrusted[fingerprints[i]] = 1
          }
        }
        /^Alias name: / { alias = substr($0, 13) }
        $1 == "SHA256:" {
          fingerprint = tolower($2)
          gsub(/:/, "", fingerprint)
          if (fingerprint in distrusted) print alias
        }
      '
}

verify_store() {
  keytool=$1
  store=$2
  remaining=$(find_distrusted_aliases "$keytool" "$store")
  if [ -n "$remaining" ]; then
    printf 'Distrusted roots remain in %s:\n%s\n' "$store" "$remaining" >&2
    return 1
  fi
}

remove_distrusted_roots() {
  keytool=$1
  store=$2
  aliases=$(find_distrusted_aliases "$keytool" "$store")
  printf '%s\n' "$aliases" | while IFS= read -r alias; do
    [ -n "$alias" ] || continue
    # Keep password-less PKCS12 stores without a password.
    "$keytool" \
      -J-Dkeystore.pkcs12.certProtectionAlgorithm=NONE \
      -J-Dkeystore.pkcs12.macAlgorithm=NONE \
      -delete -alias "$alias" -keystore "$store" -storepass changeit
  done
  verify_store "$keytool" "$store"
  chmod 0644 "$store"
}

# jlink copies lib/security/{cacerts,blocked.certs} from java.base.jmod, so patch the jmod too.
patch_java_base_jmod() {
  jdk_home=$1
  jmod_file="$jdk_home/jmods/java.base.jmod"
  work_dir=$(mktemp -d)
  extract_dir="$work_dir/extracted"
  verify_dir="$work_dir/verify"
  mkdir "$extract_dir"
  "$jdk_home/bin/jmod" extract --dir "$extract_dir" "$jmod_file"
  for section in "$extract_dir"/*/; do
    case "$(basename "$section")" in
      classes|conf|lib|bin|include|legal|man) ;;
      *) printf 'Unknown java.base.jmod section: %s\n' "$section" >&2; exit 1 ;;
    esac
  done
  test -f "$extract_dir/lib/security/cacerts"
  test -f "$extract_dir/lib/security/blocked.certs"
  cp --remove-destination "$jdk_home/lib/security/cacerts" \
    "$extract_dir/lib/security/cacerts"
  cp --remove-destination "$jdk_home/lib/security/blocked.certs" \
    "$extract_dir/lib/security/blocked.certs"

  module_version=$("$jdk_home/bin/jmod" describe "$jmod_file" \
    | awk -F '@' '/^java\.base@/ { split($2, parts, "[[:space:]]"); print parts[1]; exit }')
  test -n "$module_version"
  set -- --class-path "$extract_dir/classes" --config "$extract_dir/conf" \
    --libs "$extract_dir/lib" --module-version "$module_version"
  if [ -d "$extract_dir/bin" ]; then set -- "$@" --cmds "$extract_dir/bin"; fi
  if [ -d "$extract_dir/include" ]; then set -- "$@" --header-files "$extract_dir/include"; fi
  if [ -d "$extract_dir/legal" ]; then set -- "$@" --legal-notices "$extract_dir/legal"; fi
  if [ -d "$extract_dir/man" ]; then set -- "$@" --man-pages "$extract_dir/man"; fi

  "$jdk_home/bin/jmod" create "$@" "$work_dir/java.base.jmod"
  mkdir "$verify_dir"
  "$jdk_home/bin/jmod" extract --dir "$verify_dir" "$work_dir/java.base.jmod"
  verify_store "$jdk_home/bin/keytool" "$verify_dir/lib/security/cacerts"
  cmp "$jdk_home/lib/security/blocked.certs" "$verify_dir/lib/security/blocked.certs"
  mv "$work_dir/java.base.jmod" "$jmod_file"
  rm -rf "$work_dir"
}

jdk_count=0
for version in 8 11 17 21; do
  jdk_home="/usr/lib/jvm/zulu$version"
  [ -d "$jdk_home" ] || continue
  security_dir="$jdk_home/lib/security"
  blocked_name=blocked.certs
  if [ "$version" = 8 ]; then
    security_dir="$jdk_home/jre/lib/security"
    blocked_name=blacklisted.certs
  fi

  truststore="$security_dir/cacerts"
  test -f "$truststore"
  cp --remove-destination "$blocked_file" "$security_dir/$blocked_name"
  chmod 0644 "$security_dir/$blocked_name"
  remove_distrusted_roots "$jdk_home/bin/keytool" "$truststore"

  if [ "$version" != 8 ] && [ -f "$jdk_home/jmods/java.base.jmod" ]; then
    patch_java_base_jmod "$jdk_home"
  fi
  jdk_count=$((jdk_count + 1))
done

[ "$jdk_count" -gt 0 ]

# Ubuntu's ca-certificates-java store, used by Ubuntu's OpenJDK packages.
system_truststore=/etc/ssl/certs/java/cacerts
if [ -f "$system_truststore" ]; then
  system_keytool=/usr/lib/jvm/zulu17/bin/keytool
  [ -x "$system_keytool" ] || system_keytool=/usr/lib/jvm/zulu21/bin/keytool
  remove_distrusted_roots "$system_keytool" "$system_truststore"
fi
